
<p align="center">

<a href="https://github.com/radon-h2020/radon-defect-predictor/actions?query=workflow%3A%22Build"><img alt="GitHub Actions status" src="https://github.com/radon-h2020/radon-defect-predictor/workflows/Build/badge.svg?branch=main"></a>
<a href="https://lgtm.com/projects/g/radon-h2020/radon-defect-predictor/context:python"><img alt="Language grade: Python" src="https://img.shields.io/lgtm/grade/python/g/radon-h2020/radon-defect-predictor.svg?logo=lgtm&logoWidth=18"></a>
<a href="https://lgtm.com/projects/g/radon-h2020/radon-defect-predictor/context:python"><img alt="Total alerts" src="https://img.shields.io/lgtm/alerts/g/radon-h2020/radon-defect-predictor.svg?logo=lgtm&logoWidth=18"></a>
</p>

# radon-defect-predictor
The RADON command-line client for Infrastructure-as-Code Defect Prediction.


## How to Install

From source code:
```
git clone https://github.com/radon-h2020/radon-defect-predictor.git
cd radon-defect-predictor
pip install .
```

## Quick Start

```radon-defect-predictor --help```

```prompt
usage: radon-defect-predictor [-h] [-v] {train,predict,model} ...

A Python library to train machine learning models for defect prediction of infrastructure code

positional arguments:
  {train,predict,model}
    train               train a brand new model from scratch
    model               get a pre-trained model to test unseen instances
    predict             predict unseen instances

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
```

See the [Docs](https://radon-h2020.github.io/radon-defect-predictor/) for details and examples of usage.