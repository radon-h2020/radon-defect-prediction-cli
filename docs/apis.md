# API Reference

## train.DefectPredictor

This module includes one class, DefectPredictor, representing a defect predictor.

!!! note "class radondefectpredictor.train.DefectPredictor()"
    Class representing a defect predictor. It contains the logic to train a model, save and load a model from the disk, use that model to predict unseen instances.
    
`__init__()`

Init the DefectPredictor
    
`balancers() -> list`

Return the list of instances used to balance the train data.

`balancers(balancers:List[str]) -> None`

Set the balancers to train the model.

&emsp;&emsp;**Parameters:**&emsp;&emsp;**balancers**(List[str]) - a list of balancers (e.g.,  `[none, rus, ros]`) <br>
&emsp;&emsp;**Raise:**&emsp;&emsp;**ValueError** - if one or more balancers are not in `[none, rus, ros]`


    
`normalizers() -> list`

Return the list of instances used to normalize train and test data.

`normalizers(normalizers:List[str]) -> None`

Set the normalizers to scale data.

&emsp;&emsp;**Parameters:**&emsp;&emsp;**normalizers**(List[str]) - a list of normalizers (e.g.,  `[none, minmax, std]`) <br>
&emsp;&emsp;**Raise:**&emsp;&emsp;**ValueError** - if one or more normalizers are not in `[none, minmax, std]`


    
`classifiers()`

Return the list of instances used to train the model classifier.

`classifiers(classifiers:List[str])`

Set the balancers to train the model.

&emsp;&emsp;**Parameters:**&emsp;&emsp;**classifiers**(List[str]) - a list of classifiers (e.g.,  `[dt, logit, nb, rf, svm]`) <br>
&emsp;&emsp;**Raise:**&emsp;&emsp;**ValueError** - if one or more normalizers are not in `[dt, logit, nb, rf, svm]`



`train(data:pandas.DataFrame) -> imblearn.pipeline.Pipeline`
Train a new model

&emsp;&emsp;**Parameters:**&emsp;&emsp;**data**(pandas.DataFrame) - the train data consisting of metrics and metadata about *clean* and *failure_prone* scripts <br>
&emsp;&emsp;**Return:** the best fitted estimator, that is, the one that maximizes the average_precision <br>
&emsp;&emsp;**Raise:**&emsp;&emsp;**Fail** - if columns `failure_prone`, `commit`, `committed_at`, `filepath` are not in `data`



`predict(unseed_data:pandas.DataFrame) -> bool`
Predict an unseen instance as failure-prone or clean.

&emsp;&emsp;**Parameters:**&emsp;&emsp;**data**(pandas.DataFrame) - the unseen data consisting of the observations to predict <br>
&emsp;&emsp;**Return:** *True* if *failure-prone*; *False* otherwise <br>
&emsp;&emsp;**Raise:**&emsp;&emsp;**Exception** - if no model has been loaded.



`load_model(path_to_model_dir: str) -> None`
Load a model from the disk.

&emsp;&emsp;**Parameters:**&emsp;&emsp;**path_to_model_dir**(str) - the path to the directory containing model-related files <br>



`dump_model(path_to_model_dir: str) -> None`
Dump the trained model to the disk.

&emsp;&emsp;**Parameters:**&emsp;&emsp;**path_to_model_dir**(str) - the path to the directory where to save model-related files <br>




