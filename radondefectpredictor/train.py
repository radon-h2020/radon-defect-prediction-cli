import numpy as np
import pandas as pd
from typing import Generator, List

from imblearn.pipeline import Pipeline
from sklearn.metrics import make_scorer, matthews_corrcoef
from sklearn.feature_selection import VarianceThreshold
from sklearn.model_selection import RandomizedSearchCV

from .balancers import balancers_map
from .classifiers import classifiers_map
from .hyper_parameters import search_params_map
from .normalizers import normalizers_map
from .model_validation import walk_forward_release


class DefectPredictor:

    def __init__(self,
                 data: pd.DataFrame,
                 classifiers: List[str],
                 balancers: List[str] = None,
                 normalizers: List[str] = None):

        # TODO: add a pre-trained estimator

        self.cv_report_map = dict()
        self.best_estimator = None
        self.best_estimator_average_precision = 0
        self.selected_features = list()

        self.X = self.y = pd.DataFrame()
        self.classifiers = classifiers
        self.balancers = balancers
        self.normalizers = normalizers

        self.__prepare_data(data)
        self.__pipeline_sanity_check()

    def __prepare_data(self, data: pd.DataFrame):
        assert 'failure_prone' in data.columns
        assert 'commit' in data.columns
        assert 'committed_at' in data.columns
        assert 'filepath' in data.columns
        assert 'repository' in data.columns

        data = data.fillna(0)

        # Create a column group to group observations of the same release (identified by the commit)
        data['group'] = data.commit.astype('category').cat.rename_categories(range(1, data.commit.nunique() + 1))

        # Make sure the data is sorted by commit time (ascending)
        data.sort_values(by=['committed_at'], ascending=True)
        data = data.reset_index(drop=True)

        # Remove metadata
        data = data.drop(['commit', 'committed_at', 'filepath', 'repository'], axis=1)

        self.X, self.y = data.drop(['failure_prone'], axis=1), data.failure_prone.values.ravel()

    def __pipeline_sanity_check(self):

        for balancer in self.balancers:
            if balancer not in ('none', 'rus', 'ros'):
                raise ValueError(f'{balancer} is not supported')

        for normalizer in self.normalizers:
            if normalizer not in ('none', 'minmax', 'std'):
                raise ValueError(f'{normalizer} is not supported')

        for classifier in self.classifiers:
            if classifier not in ('decision-tree', 'logistic-regression', 'naive-bayes', 'random-forest', 'svm'):
                raise ValueError(f'{classifier} is not supported')

    def train(self) -> Pipeline:
        """
        Return the best fitted estimator, that is, the one that maximizes the average_precision
        :yield: the cross-validation reporto for every classifier
        :return: an estimator of type Pipeline
        """
        scoring = dict(
            roc_auc='roc_auc',
            average_precision='average_precision',
            accuracy='accuracy',
            balanced_accuracy='balanced_accuracy',
            precision='precision',
            recall='recall',
            f1='f1',
            mcc=make_scorer(matthews_corrcoef)
        )

        for classifier in self.classifiers:
            estimator = classifiers_map[classifier]

            pipe = Pipeline([
                ('variance', VarianceThreshold(threshold=0)),  # Remove constant features
                ('balancing', None),  # To balance the training data See search_params['balancing'] below)
                ('normalization', None),  # To scale (and center) data. See search_params['normalization'] below
                # TODO feature_selection here
                ('classification', estimator)
            ])

            releases = self.X.group.tolist()
            X_local = self.X.drop(['group'], axis=1)

            search_params = search_params_map[classifier]

            if self.balancers:
                search_params['balancing'] = [balancers_map[balancer] for balancer in self.balancers]

            if self.normalizers:
                search_params['normalization'] = [normalizers_map[normalizer] for normalizer in self.normalizers]

            search = RandomizedSearchCV(pipe, search_params, cv=walk_forward_release(X_local, self.y, releases),
                                        scoring=scoring, refit='average_precision', verbose=0)

            search.fit(X_local, self.y)

            # Add additional metadata to the cv_results
            search.cv_results_['best_index_'] = search.best_index_
            search.cv_results_['n_features'] = X_local.shape[1]
            search.cv_results_['y_0'] = self.y.tolist().count(0)
            search.cv_results_['y_1'] = self.y.tolist().count(1)

            self.cv_report_map[classifier] = search.cv_results_

            # Get the highest average_precision for this randomized search
            local_best_average_precision = search.cv_results_['mean_test_average_precision'][search.best_index_]

            if (not self.best_estimator) or local_best_average_precision > self.best_estimator_average_precision:
                self.best_estimator = search.best_estimator_
                selected_features_indices = self.best_estimator.named_steps['variance'].fit(X_local).get_support(
                    indices=True)
                self.selected_features = X_local.iloc[:, selected_features_indices].columns.tolist()

        return self.best_estimator

    def predict(self, X:pd.DataFrame) -> bool:
        """
        Predict an unseen instance as failure-prone or clean.
        :param X: pandas DataFrame containing the observation to predict
        :return: True if failure-prone. False, otherwise.
        """
        # Select same model features
        test_instance = X[np.intersect1d(X.columns, self.selected_features)]

        # Perform pre-process if any
        if self.best_estimator.named_steps['normalization']:
            test_instance = pd.DataFrame(self.best_estimator.named_steps['normalization'].transform(test_instance))

        clf = self.best_estimator.named_steps['classification']
        prediction = bool(clf.predict(test_instance)[0])

        return prediction

    """
    def to_pickle(self, return_string=True, filepath: str = None):

        if filepath:
            joblib.dump(self.best_estimator, filepath)
            joblib.dump(self.selected_features, filepath)
            # TODO save attributes

        if return_string or not filepath:
            # return jsonpickle.encode(pipeline_pkl)
            buf = io.BytesIO()
            joblib.dump(self.best_estimator, buf)
            return buf
    """