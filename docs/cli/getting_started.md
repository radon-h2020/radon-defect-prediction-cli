# Getting Started

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
    `radon-defect-predictor predict` **MUST** be used after having trained a model with 
    `radon-defect-predictor train`, or after having downloaded a pre-trained model from the online RADON 
    Defect Prediction Framework APIs, using the `radon-defect-predictor download-model` command.

Go the next pages for examples of usage of each of the command-line options.




## A quick start with Docker

First, create a host volume to share data and results between the host machine and the Docker container:

`mkdir /tmp/radon-dp-volume/` (you can name it as you please)
 
### Train

Create a training dataset `metrics.csv` and copy/move it to `/tmp/radon-dp-volume/`.
See how to generate the training data for defect prediction [here](https://radon-h2020.github.io/radon-repository-miner/cli/metrics/). 

Run:

`docker run -v /tmp/radon-dp-volume:/app radon-dp:latest radon-defect-predictor train metrics.csv ...`

See the [docs](https://radon-h2020.github.io/radon-defect-prediction-cli/cli/train/) for more details about this command. 

The built model can be accessed at `/tmp/radon-dp-volume/radondp_model.joblib`.



### Model

Run:

`docker run -v /tmp/radon-dp-volume:/app radon-dp:latest radon-defect-predictor download-model ...`

See the [docs](https://radon-h2020.github.io/radon-defect-prediction-cli/cli/model/) for more details about this command. 

The downloaded model can be accessed at `/tmp/radon-dp-volume/radondp_model.joblib`.



### Predict

Move the model and the files to predict in the shared volume.
For example, if you want to run the prediction on a .csar, then

`cp patah/to/file.csar /tmp/radon-dp-volume`.

Alternatively, you can create a volume from the folder containing the .csar (in that case, make sure to move the model within it).

Run:

`docker run -v /tmp/radon-dp-volume:/app radon-dp:latest radon-defect-predictor predict ...`

See the [docs](https://radon-h2020.github.io/radon-defect-prediction-cli/cli/predict/) for more details about this command. 

The predictions can be accessed at `/tmp/radon-dp-volume/radondp_predictions.json`.

