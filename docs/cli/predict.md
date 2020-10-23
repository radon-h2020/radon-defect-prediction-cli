# Predict unseen instances


```text
usage: radon-defect-predictor predict [-h] language path_to_artefact

positional arguments:
  {ansible,tosca}   the language of the file (i.e., TOSCA or YAML-based Ansible)
  path_to_artefact  the path to the artefact to analyze (i.e., an Ansible or Tosca file or .csar

optional arguments:
  -h, --help            show this help message and exit

```


!!! note "Output"
    This command will generate a **`radondp_predictions.json`** file in the user working directory.
    The file contains information about the *filepath*, *failure-proneness*, and *date* of analysis of the analyzed files.
    If a file already exists with that name, this command will **append** the new predictions to it.

    **Note:** To let the tool automatically identify the model, the user **must** run the command within the same working
    directory of `radondp_model.joblib`.
    Make sure you trained or downloaded a model first. 


## language
The language of the file to analyze (that is Ansible or Tosca).
This is needed to automatically extract the proper metrics (through ```radon-ansible-metrics```(https://github.com/radon-h2020/radon-ansible-metrics) or ```radon-tosca-metrics```(https://github.com/radon-h2020/radon-tosca-metrics)) to pass to the predictor.  

## path_to_artefact

The path to the artefact to analyze.
An *artefact* can be an Ansible file (**.yml**), a TOSCA definition (**.tosca**), or a TOSCA Cloud Service Archive(**.csar**).


## Examples

### Predict on a single script

For the sake of example, move to the `radon_example` working directory.
If you do not have a model, [train](https://radon-h2020.github.io/radon-defect-prediction-cli/cli/train/#Example)
or [download](https://radon-h2020.github.io/radon-defect-prediction-cli/cli/model/#Examples) one first.

* Download [playbook.yml](https://radon-h2020.github.io/radon-defect-prediction-cli/examples_resources/playbook.yml) to test 
an Ansible model.

* Download [definition.tosca](https://radon-h2020.github.io/radon-defect-prediction-cli/examples_resources/definition.tosca)
to test a Tosca model.

* Download [tosca.csar](https://radon-h2020.github.io/radon-defect-prediction-cli/examples_resources/tosca.csar)
to test a Tosca model.


Copy the file(s) in `radon_example`.

Then, run:

`radon-defect-predictor predict ansible playbook.yml` (for Ansible)

`radon-defect-predictor predict tosca definition.yml` (for Tosca)

`radon-defect-predictor predict tosca tosca.csar` (for Tosca CSAR)

You can now see the results:

```text
ls

prediction_results.json
```

### Predict on a .CSAR
Create a working directory:

```text
mkdir csar_example
cd csar_example
```

Download the following [tosca.csar] and a pre-trained model as described [here] in *csar_example*.

Create folder for reports: `mkdir reports`

Then run:

`radon-defect-predictor predict --path-to-model downloaded_model --path-to-artefact tosca.csar -l ansible --d reports`

You can now see the report:

```text
cd predictions
ls

prediction_results.json
```