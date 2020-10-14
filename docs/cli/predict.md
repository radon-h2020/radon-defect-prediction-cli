# Predict unseen instances

```radon-defect-predictor predict```

```prompt
usage: radon-defect-predictor predict [-h] --path-to-model PATH_TO_MODEL_DIR --path-to-file PATH_TO_FILE -l {ansible,tosca} -d DEST

optional arguments:
  -h, --help            show this help message and exit


  --path-to-model PATH_TO_MODEL_DIR
                        path to the folder containing the files related to the model
  --path-to-file PATH_TO_FILE
                        the path to the file to analyze
  -l {ansible,tosca}, --language {ansible,tosca}
                        the language of the file (i.e., TOSCA or YAML-based Ansible)
  -d DEST, --destination DEST
                        destination folder to save the prediction report
```

| Option | Required |
|:---|:---|
| --path-to-model | True |
| --path-to-file | True |
| -l, --language | True |
| -d, --destination | True |


<br>

**Return:**

* ```exit(0)``` if the file is predicted *clean*;

* ```exit(1)``` if the file is predicted *failure-prone*.

<br>


**Important!** Make sure you trained a model using or downloaded a pre-trained model using , first. 

## --path-to-model 

**```radon-defect-predictor predict --path-to-model path/to/model/```**

The path to the **folder** containing files related to a model (model, selected_features and report).
The folder has to be structured as follows:

*path/to/*<br>
&emsp;|- *model/*<br>
&emsp;&emsp;|- *model.pkl*<br>
&emsp;&emsp;|- *model_features.json*<br>
&emsp;&emsp;|- *report.json*<br>

Information about the aforementioned files can be found [here](https://radon-h2020.github.io/radon-defect-predictor/cli/train/#-d-destination) or [here](https://radon-h2020.github.io/radon-defect-predictor/cli/model/#-d-destination).


## --path-to-file
**```radon-defect-predictor train --path-to-csv path/to/repository-data.csv```**

The path to the **.yml or .tosca** file analyze.


## -l, --language
**```radon-defect-predictor predict --l ansible```** <br>
**```radon-defect-predictor predict --l tosca```**

The language of the file to analyze (that is Ansible or Tosca).
This is needed to automatically extract the proper metrics (through ```radon-ansible-metrics```(https://github.com/radon-h2020/radon-ansible-metrics) or ```radon-tosca-metrics```(https://github.com/radon-h2020/radon-tosca-metrics)) to pass to the predictor.  


## -d, --destination 
**```radon-defect-predictor predict --d path/to/results/```**

The path to the **folder** where to log the results

* ```path/to/model-info/model.pkl``` - the exported model in pickle format. After training a model, it is desirable to have a way to persist the model for future use without having to retrain. 

* ```path/to/model-info/model_features.json``` - the features selected by feature selection during training. It is important to track these features so to reduce the *test instances* to the same set of features used for training. 

* ```path/to/model-info/report.json``` - the cross-validation report of model training.

**Important!** 

* Do not delete any of these files if you want to test new instances with the [```radon-defect-predictor predict```](https://radon-h2020.github.io/radon-defect-predictor/cli/predict/) using the downloaded model.

* Make sure you save the model and related files to a distinct folder for each repository and language (i.e., Ansible and Tosca) to avoid conflicts with existing models, features and reports.
Use the same folder only if you are overriding a model. The downloaded model will replace the existing one.

<br>

## Examples