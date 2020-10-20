# Download a pre-trained model

```radon-defect-predictor model```

```text
usage: radon-defect-predictor model [-h] {download} ...

positional arguments:
  {download}
    download       Download a pre-trained model from the online APIs

optional arguments:
  -h, --help       show this help message and exit
```


## Download from APIs
```radon-defect-predictor model download ...```

```text
usage: radon-defect-predictor model download [-h] --path-to-repository PATH_TO_REPOSITORY --host {github,gitlab} [-t TOKEN] -l {ansible,tosca} -d DEST

optional arguments:
  -h, --help            show this help message and exit
  --path-to-repository PATH_TO_REPOSITORY
                        path to the cloned repository
  --host {github,gitlab}
                        whether the repository is hosted on Github or Gitlab
  -t TOKEN, --token TOKEN
                        the Github or Gitlab personal access token
  -o, --owner REPOSITORY_OWNER
                        the repository owner
  -n, --name REPOSITORY_NAME
                        the repository name
  -l {ansible,tosca}, --language {ansible,tosca}
                        the language of the file (i.e., TOSCA or YAML-based Ansible)
  -d DEST, --destination DEST
                        destination folder to save the model
```

| Option | Required |
|:---|:---|
| --path-to-repository | True |
| --host | True |
| -o --owner | True |
| -n --name | True |
| -t, --token | True |
| -l, --language | True |
| -d, --destination | True |

<br>

### --path-to-repository 
**```radon-defect-predictor model download --path-to-csv path/to/local/git/repository/```**

The path to the a local **git repository**. <br>
It is necessary to select the appropriate model for the repository at hand.
Indeed, the downloaded model is the model trained on the most similar repository based on the following criteria: 

* **Core contributors:** the number of contributors whose total number of commits accounts for 80% or more of the total contributions.
* **Continuous integration (CI):** the repository has evidence of a CI service, determined by the presence of a configuration file required by that service (e.g., a.travis.ymlfor TravisCI).
* **Comments ratio:** ratio between comments and lines of code.
* **Commit frequency:** the average number of commits per month.
* **Issue frequency:** the average number of issue events transpired per month.
* **License availability:** the repository has evidence of a license (i.e., a LICENSE file).
* **Lines of Code:** the number of executable lines of code. 
* **Ratio of IaC scripts:** ratio between Infrastructure-as-Code (IaC) files and total files.

The value of each criterion is automatically extracted by the [```radon-repository-scorer```](https://github.com/radon-h2020/radon-repository-scorer) this tool depends on. <br>


### --host
```radon-defect-predictor model download --host github``` <br>
```radon-defect-predictor model download --host gitlab```

The hosting platform for software development and version control using Git. Github and Gitlab are supported.
This option is required to use the appropriate APIs ([```pygithub```](https://github.com/PyGithub/PyGithub) or [```python-gitlab```](https://github.com/python-gitlab/python-gitlab)) to compute some of the aforementioned criteria.

### -t, --token
```radon-defect-predictor model download -t <SECRET_TOKEN>``` <br>

The personal access token to access Github and Gitlab APIs.
See how to get one from [Github](https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/creating-a-personal-access-token) and [Gitlab](https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html). <br>
Once generated, pass the token to the ```--token``` option. <br>
If not passed in the command, the user will be prompt for inserting one. For example:

```text
radon-defect-predictor model download --path-to-repository some/path --host github -l ansible -d some/other/path/
Github access token: ***************
```

!!! note "Planned! Not currently supported"
    You may want to avoid the previous step. If so, add the following to your environment variables:
    
    * ```GITHUB_ACCESS_TOKEN=<paste here your token>``` for Github, and/or
    
    * ```GITLAB_ACCESS_TOKEN=<paste here your token>``` for Gitlab.

 
### -o, --owner
```radon-defect-predictor model download -o radon-h2020``` <br>
 
### -n, --name
```radon-defect-predictor model download -o radon-defect-predictor``` <br>
 
 
### -l, --language
```radon-defect-predictor model download -l ansible``` <br>
```radon-defect-predictor model download -l tosca```

Every models are trained for a specific language. 
To download the proper model the user must specify the language (s)he wants to apply it to.
Ansible and TOSCA are currently supported.
If the project contains both Ansible and Tosca files, the user can download two models by running the command twice, passing the optiion ```-l ansible``` and ```-l tosca```, respectively.


### -d, --destination 
```radon-defect-predictor train --d path/to/model-info/```

The path to the **folder** where to download the following files about the model:

* ```path/to/model-info/model.pkl``` - the exported model in pickle format. After training a model, it is desirable to have a way to persist the model for future use without having to retrain. 

* ```path/to/model-info/model_features.json``` - the features selected by feature selection during training. It is important to track these features so to reduce the *test instances* to the same set of features used for training. 

* ```path/to/model-info/model_report.json``` - the cross-validation report of model training.

!!! note "Important!" 
    * Do not delete any of these files if you want to test new instances with the [```radon-defect-predictor predict```](https://radon-h2020.github.io/radon-defect-predictor/cli/predict/) using the downloaded model.
    
    * Make sure you save the model and related files to a distinct folder for each repository and language (i.e., Ansible and Tosca) to avoid conflicts with existing models, features and reports.
    Use the same folder only if you are overriding a model. The downloaded model will replace the existing one.

<br>

    
### Examples

Git clone the repository to analyze, say **ansible-community/molecule**:

`git clone https://github.com/ansible-community/molecule.git`

Create a new folder to save the downloaded mode-related files and run the `radon-defect-predictor model download` command:

```text
cd molecule
mkdir downloaded_model
```

Then, run:

`radon-defect-predictor model download --path-to-repository . --host github -t ***** -o ansible-community -n molecule -l ansible -d downloaded_model`

You should be now able to see the following files:

```text
cd downloaded_model
ls

model.pkl model_features.json
```