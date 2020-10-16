## Getting Started

```radon-defect-predictor```

```text
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

!!! warning 
    ```radon-defect-predictor predict``` **must** be used after having trained a model with 
    ```radon-defect-predictor train```, or after having loaded a pre-trained model from the disk or from the online RADON 
    Defect Prediction Framework APIs, using the ```radon-defect-predictor model``` command.

Go the next pages for examples of usage of each of the three command-line options.