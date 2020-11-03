# RADON Defect Predictor

The RADON Defect Predictor is a Python library and a command-line tool to train and use Machine-Learning models for infrastructure code defect prediction.

## How to install

From PyPIP: **available soon**


From source code:

```text
git clone https://github.com/radon-h2020/radon-defect-prediction.git
cd radon-defect-predictor
pip install .
```


## How to test

```text
pip install pytest
unzip test_data.zip -d .
pip install .
GITHUB_ACCESS_TOKEN=************
GITLAB_ACCESS_TOKEN=******
pytest tests/
```
