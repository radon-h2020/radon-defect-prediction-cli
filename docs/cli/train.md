# Train a new model from scratch

```text
usage: radon-defect-predictor train [-h] [--balancers BALANCERS] [--normalizers NORMALIZERS] path_to_csv classifiers

positional arguments:
  path_to_csv           the path to the csv file containing the data for training
  classifiers           a list of classifiers to train. Possible choices [dt, logit, nb, rf, svm]


optional arguments:
  -h, --help            show this help message and exit
  --balancers BALANCERS
                        a list of balancer to balance training data. Possible choices [none, rus, ros]
  --normalizers NORMALIZERS
                        a list of normalizers to normalize data. Possible choices [none, minmax, std]
```

!!! note "Output"
    This command will generate a **`radondp_model.joblib`** file in the user working directory.
    The file contains information about the best estimator, subset of features selected by the training, and the results
    of cross-validation.
    
    **Note:** The *radondp_model.joblib* will override the existing one in the user working directory, if any.  



<br>

## path_to_csv 
**```radon-defect-predictor train --path-to-csv path/to/repository-data.csv```**

The path to the training data (a **.csv** file). 
You can generate training data for IaC defect-prediction through [radon-miner](https://github.com/radon-h2020/radon-repository-miner/).
An example observation is the following:

| filepath | commit | committed_at | failure_prone | metric_1 | ... | metric_n |
|:---|:---|:---|:---|:---|:---|:---|
|roles/tasks/main.yml | 25c04... | 1526444640 | 1 | value_1 | ... | value_n |

* ```filepath: string``` is the path to the file from the repository root;
* ```commit: string``` is the commit sha the file belongs to. In per-release based defect-prediction, it is the commit sha of a release, and it is used to group observations of the same release;
* ```committed_at: string``` is the commit datetime. In release-based defect-prediction, it is the release date. In just-in-time defect-prediction is the commit date. It is used to sort releases/commits for walk-forward validation;
* ```failure_prone: integer``` **1** if the observation is **failure-prone**; 0 otherwise;
* ```metric_i: float``` a metric.

!!! warning 
    Missing one of the following columns will raise an error: ```filepath```, ```commit```, ```committed_at```, ```failure_prone```. 

## classifiers 

**```radon-defect-predictor train --classifiers="dt logit nb rf svm"```**

* ```dt``` - Train a model using a **[sklearn.tree.DecisionTreeClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html)** classifier;

* ```logit``` - Train a model using a **[sklearn.linear_model.LogisticRegression](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html)** classifier;

* ```nb``` - Train a model using a **[sklearn.naive_bayes.GaussianNB](https://scikit-learn.org/stable/modules/generated/sklearn.naive_bayes.GaussianNB.html)** classifier;

* ```rf``` - Train a model using a **[sklearn.ensemble.RandomForestClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html)** classifier;

* ```svm``` - Train a model using a **[sklearn.tree.DecisionTreeClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html)** classifier.


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






## Example

Assuming we are training a new model for the [ansible-community/molecule](https://github.com/ansible-community/molecule) project,
download the following training set [molecule.csv](https://radon-h2020.github.io/radon-defect-prediction-cli/examples_resources/molecule.csv)
generated using [radon-miner](https://github.com/radon-h2020/radon-repository-miner/).
This is the "ground truth" to train a model for that project. 

You can now run the `radon-defect-predictor train ...` wherever on your system. 
For the sake of example, let's create and move to a new working directory:

```text
mkdir radon_example
cd radon_example
mv /home/<user>/Downloads/molecule.csv .
```

Now run:

`radon-defect-predictor train molecule.csv  "dt logit" --balancers "none rus" --normalizers "minmax"`

or (equivalent)

`radon-defect-predictor train molecule.csv  "dt logit" -b "none rus" -n "minmax"`

The previous command loads and prepares the *.csv* file. Then, it builds a model using:

* the Decision Tree and Logistic Regression classifiers (`"dt logit"`);
* the Random Under-Sampling technique to balance the training data (```rus```), or none (```none```);
* the minmax normalization to scale data within the range [0,1] (```minmax```).


The built model (`model.pkl`), selected features (`features.json`), and cross-validation report (`report.json`) are saved into `radondp_model.zip`.
You can see it by running:

```text
ls

molecule.csv
radondp_model.joblib
```   

![Alt Text](../media/cli_train.gif)

You can run the same command with different combinations of balancers, normalizers, and classifiers, as explained in 
previous sections.