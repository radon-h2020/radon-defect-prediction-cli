# Train a new model from scratch
```radon-defect-predictor train```

```prompt
usage: radon-defect-predictor train [-h] --path-to-csv PATH_TO_CSV [--balancers BALANCERS] [--normalizers NORMALIZERS] --classifiers CLASSIFIERS -d DEST

optional arguments:
  -h, --help            show this help message and exit
  --path-to-csv PATH_TO_CSV
                        the path to the csv file containing the data for training
  --balancers BALANCERS
                        a list of balancer to balance training data. Possible choices [none, rus, ros]
  --normalizers NORMALIZERS
                        a list of normalizers to normalize data. Possible choices [none, minmax, std]
  --classifiers CLASSIFIERS
                        a list of classifiers to train. Possible choices [decision-tree, logit, naive-bayes, random-forest, svm]
  -d DEST, --destination DEST
                        destination folder to save the model and reports
```

| Option | Required |
|:---|:---|
| --path-to-csv | True |
| --balancers | False |
| --normalizers | False |
| --classifiers | True |
| -d, --destination | True |

<br>

## --path-to-csv 
**```radon-defect-predictor train --path-to-csv path/to/repository-data.csv```**

The path to the **.csv** file containing observations to train the model. Observations are metrics for every script in the repository at each release.
An example observation is the following:

| filepath | commit | committed_at | failure_prone | metric_1 | ... | metric_n |
|:---|:---|:---|:---|:---|:---|:---|
|roles/tasks/main.yml | 25c04... | 1526444640 | 1 | value_1 | ... | value_n |

* ```filepath: string``` is the path to the file from the repository root;
* ```commit: string``` is the commit sha the file belongs to. In per-release based defect-prediction, it is the commit sha of a release, and it is used to group observations of the same release;
* ```committed_at: integer``` is the timestamp of the commit date. In per-release based defect-prediction, it is the release date. It is used to sort releases for walk-forward validation;
* ```failure_pront: integer``` 1 if the observation is **failure-prone**; 0 otherwise;
* ```metric_i: float``` a metric.

**Note:** Lacking one of the following columns will raise an error: ```filepath```, ```commit```, ```committed_at```, ```failure_prone```. 


## --balancers 

**```radon-defect-predictor train --balancers="none rus ros"```**

* ```none``` - Do not balance training data;

* ```rus``` - Do balance training data using **Random Under-Sampling**;

* ```ros``` - Do balance training data using **Random Over-Sampling**.

Not providing any options is the same as passing the option ```none```.
However, this option can be passed along the others to train the model by either balancing and not balancing the training set. 



## --normalizers 

**```radon-defect-predictor train --normalizers="none minmax std"```**

* ```none``` - Do not normalize training data;

* ```minmax``` - Transform features by scaling each feature to the range [0,1]. It uses the **[sklearn.preprocessing.MinMaxScaler](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.MinMaxScaler.html)**;

* ```std``` - Standardize features by removing the mean and scaling to unit variance. It uses the **[sklearn.preprocessing.StandardScaler](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html)**.

Not providing any options is the same as passing the option ```none```.
However, this option can be passed along the others to train the model by either normalizing and not normalizing the training set. 



## --classifiers 

**```radon-defect-predictor train --classifiers="dt logit nb rf svm"```**

* ```dt``` - Train a model using a **[sklearn.tree.DecisionTreeClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html)** classifier;

* ```logit``` - Train a model using a **[sklearn.linear_model.LogisticRegression](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html)** classifier;

* ```nb``` - Train a model using a **[sklearn.naive_bayes.GaussianNB](https://scikit-learn.org/stable/modules/generated/sklearn.naive_bayes.GaussianNB.html)** classifier;

* ```rf``` - Train a model using a **[sklearn.ensemble.RandomForestClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html)** classifier;

* ```svm``` - Train a model using a **[sklearn.tree.DecisionTreeClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html)** classifier.



## -d, --destination 
**```radon-defect-predictor train --d path/to/report/```**

The path to the **folder** where to save training report and the fitted model.
It generates the following files:

* ```path/to/report/model.pkl``` - the exported model in pickle format. After training a model, it is desirable to have a way to persist the model for future use without having to retrain. 

* ```path/to/report/model_features.json``` - the features selected by feature selection during training. It is important to track these features so to reduce the *test instances* to the same set of features used for training. 

* ```path/to/report/model_report.json``` - the cross-validation report of model training.

**Important!** 

* Do not delete any of these files if you want to test new instances with the [```radon-defect-predictor predict```](https://radon-h2020.github.io/radon-defect-predictor/cli/predict/) using the trained model.

* Make sure you create a distinct folder for each repository to avoid conflicts with existing models, features and reports.
Use the same folder only if you are re-training a model. The new model will replace the existing one only if its *average precision* (a.k.a. AUC-PR) is higher than the one of the current model (present in *path/to/report/model_report.json*).  


## Examples

Download the following [training set](https://radon-h2020.github.io/radon-defect-predictor/examples_resources/molecule.csv) generated from the [ansible-community/molecule](https://github.com/ansible-community/molecule) project in ```path/to/molecule.csv```.
This is the "ground truth" to train a model for that project. 

Create a new foler for reports:

```
cd path/to/
mkdir molecule_reports
```

Then, run:

```
radon-defect-predictor train --path-to-csv path/to/molecule.csv --balancers "none rus" --normalizers "minmax" --classifiers "dt logit" -d path/to/molecule_reports/
```

This command loads the csv file and prepares it for training.

Afterwards, it (1) uses the Random Under-Sampling balancer to balance the training data (```rus```), or none (```none```);
(2) normalizes the data within the range [0,1] (```minmax```); and (3) uses the DecisionTree and LogisticRegression classifiers (```dt logit``` , respectively).

Finally, the best model (```model.pkl```), selected features (```model_features.json```), and cross-validation report (```model_report.json```) are saved into ```path/to/molecule_reports/```.
You can see them by running

```
cd molecule_reports
ls
```   

You can run the same command with different combinations of balancers, normalizers, and classifiers, as explained in 
previous sections.