# Predict unseen instances

```radon-defect-predictor predict```

```text
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


!!! note "Important!" 
    Make sure you trained a model using or downloaded a pre-trained model using, first. 

## --path-to-model 

```radon-defect-predictor predict --path-to-model path/to/model/```

The path to the **folder** containing files related to a model (model, selected_features and report).
The folder has to be structured as follows:

```text
path/to/
  |- model/
    |- model.pkl
    |- model_features.json
    |- model_report.json
```
    
Information about the aforementioned files can be found [here](https://radon-h2020.github.io/radon-defect-predictor/cli/train/#-d-destination) or [here](https://radon-h2020.github.io/radon-defect-predictor/cli/model/#-d-destination).


## --path-to-file
```radon-defect-predictor train --path-to-csv path/to/repository-data.csv```

The path to the **.yml or .tosca** file analyze.


## -l, --language
```radon-defect-predictor predict --l ansible``` <br>
```radon-defect-predictor predict --l tosca```

The language of the file to analyze (that is Ansible or Tosca).
This is needed to automatically extract the proper metrics (through ```radon-ansible-metrics```(https://github.com/radon-h2020/radon-ansible-metrics) or ```radon-tosca-metrics```(https://github.com/radon-h2020/radon-tosca-metrics)) to pass to the predictor.  


## -d, --destination 
```radon-defect-predictor predict --d path/to/results/```

The path to the **folder** where to log the results. It will save the following file:

*  ```path/to/results/prediction_results.json``` - a json file with the following schema:

```text
{ 
  file=<string>,
  failure_prone=<boolean>,
  analyzed_at=<string> 
}
```

**Note:** if the file already exists, it will modified in **appended mode**. The field ```analyzed_at``` (YYYY-MM-DD) helps 
to track the predictions over time for each analyzed file.
<br>

## Examples

Download a pre-trained model as described [here](https://radon-h2020.github.io/radon-defect-predictor/cli/model/#Examples).
Create folder for reports: `mkdir predictions`
Then run:

`radon-defect-predictor predict --path-to-model path/to/downloaded_model --path-to-file path/to/ansible_file.yml -l ansible --d path/to/predictions`

You can now see the report:

```text
cd predictions
ls

prediction_results.json
```