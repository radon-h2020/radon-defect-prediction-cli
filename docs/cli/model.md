# Download a pre-trained model

!!! warning
    This command is partially implemented.

```text
usage: radon-defect-predictor download-model [-h] {ansible,tosca} {github,gitlab} repository

positional arguments:
  {ansible,tosca}  the language the model is trained on
  {github,gitlab}  the platform the user's repository is hosted to
  repository       the user's remote repository in the form <namespace>/<repository> (e.g., radon-h2020/radon-defect-prediction-cli)

optional arguments:
  -h, --help       show this help message and exit
```

!!! warning
    It is important to set up the following variables in your environment:
    
    * `GITHUB_ACCESS_TOKEN=<paste your token here>` for Github, and/or
    
    * `GITLAB_ACCESS_TOKEN=<paste your token here>` for Gitlab.
    
    * `TMP_REPOSITORIES_DIR=/tmp/` if not using the Docker image. It is the directory where the tool clones the repository
    to extract the information to get the best matching model.


## language {ansible, tosca}
Every models are trained for a specific language. 
To download the proper model the user **must** specify the language on which they want to use the model.
Ansible and TOSCA are currently supported.
If the project contains both Ansible and Tosca files, the user can download two models by running the command twice, 
passing the option `ansible` and `tosca`, respectively.


## host {github, gitlab}
The hosting platform for software development and version control using Git. Github and Gitlab are supported.
This option is required to use the appropriate APIs ([```pygithub```](https://github.com/PyGithub/PyGithub) or 
[```python-gitlab```](https://github.com/python-gitlab/python-gitlab)) to compute some of the aforementioned criteria.


## repository 

The user's repository full name *namespace/repository* (e.g., radon-h2020/radon-defect-prediction-cli). <br>
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


    
## Examples

### Ansible

Let's assume the user wants to download an Ansible model suitable for [ANXS/postgresql](https://github.com/ANXS/postgresql.git).

For the sake of the example, let's create and move to a working directory:

`mkdir radon-wd-ansible && cd radon-wd-ansible`

The user can now get an Ansible model by running:
 
`radon-defect-predictor download-model ansible github ANXS/postgresql`

The model is saved in the current working directory:

```text
ls

radondp_model.joblib
```

The model can be used later for predictions.


### Tosca

Let's assume the user wants to download a TOSCA model suitable for [UoW-CPC/COLARepo](https://github.com/UoW-CPC/COLARepo.git).

For the sake of the example, let's create and move to a working directory:

`mkdir radon-wd-tosca && cd radon-wd-tosca`

The user can now get an Ansible model by running:
 
`radon-defect-predictor download-model tosca github UoW-CPC/COLARepo`

The model is saved in the current working directory:

```text
ls

radondp_model.joblib
```

The model can be used later for predictions. 