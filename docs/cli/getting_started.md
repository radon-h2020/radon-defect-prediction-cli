## Getting Started

```text
usage: radon-defect-predictor [-h] [-v] {train,download-model,predict} ...

A Python library to train machine learning models for defect prediction of infrastructure code

positional arguments:
  {train,download-model,predict}
    train               Train a brand new model from scratch
    download-model      Download a pre-trained model from the online APIs
    predict             Predict unseen instances

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
```

!!! warning 
    `radon-defect-predictor predict` **must** be used after having trained a model with 
    `radon-defect-predictor train`, or after having downloaded a pre-trained model from the online RADON 
    Defect Prediction Framework APIs, using the `radon-defect-predictor download-model` command.

Go the next pages for examples of usage of each of the command-line options.