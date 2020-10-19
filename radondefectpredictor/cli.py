import datetime
import io
import json
import os
import pandas as pd

from ansiblemetrics import metrics_extractor
from argparse import ArgumentParser, ArgumentTypeError, Namespace

from .train import DefectPredictor


def valid_dir(x: str) -> str:
    """
    Check the directory exists
    :param x: a path
    :return: the path if exists; raise an ArgumentTypeError otherwise
    """
    if not os.path.isdir(x):
        raise ArgumentTypeError('Insert a valid path')

    return x


def valid_file(x: str) -> str:
    """
    Check the file exists
    :param x: a path
    :return: the path if exists; raise an ArgumentTypeError otherwise
    """
    if not os.path.isfile(x):
        raise ArgumentTypeError('Insert a valid path')

    return x


def valid_balancers(x: str):
    """
    Check x is a list of valid balancers
    :param x: a string representing a list of balancers (e.g., "none rus ros")
    :return: the list of balancers if every argument in x is a valid balancer; raise an ArgumentTypeError otherwise
    """
    balancers = x.split(' ')
    for balancer in balancers:
        if balancer not in ('none', 'rus', 'ros'):
            raise ArgumentTypeError(f'{balancer} is not a valid argument')

    return balancers


def valid_normalizers(x: str):
    """
    Check x is a list of valid normalizers
    :param x: a string representing a list of normalizers (e.g., "none minmax std")
    :return: the list of normalizers if every argument in x is a valid normalizer; raise an ArgumentTypeError otherwise
    """
    normalizers = x.split(' ')
    for normalizer in normalizers:
        if normalizer not in ('none', 'minmax', 'std'):
            raise ArgumentTypeError(f'{normalizer} is not a valid argument')

    return normalizers


def valid_classifiers(x: str):
    """
    Check x is a list of valid classifiers
    :param x: a string representing a list of classifiers (e.g., "dt logit nb rf svm")
    :return: the list of classifiers if every argument in x is a valid classifier; raise an ArgumentTypeError otherwise
    """
    classifiers = x.split(' ')
    for classifier in classifiers:
        if classifier not in ('dt', 'logit', 'nb', 'rf', 'svm'):
            raise ArgumentTypeError(f'{classifier} is not a valid argument')

    return classifiers


def set_train_parser(subparsers):
    parser = subparsers.add_parser('train', help='Train a brand new model from scratch')
    parser.add_argument('--path-to-csv',
                        required=True,
                        action='store',
                        dest='path_to_csv',
                        type=valid_file,
                        help='the path to the csv file containing the data for training')

    parser.add_argument('--balancers',
                        required=False,
                        dest='balancers',
                        type=valid_balancers,
                        help='a list of balancer to balance training data. Possible choices [none, rus, ros]')

    parser.add_argument('--normalizers',
                        required=False,
                        dest='normalizers',
                        type=valid_normalizers,
                        help='a list of normalizers to normalize data. Possible choices [none, minmax, std]')

    # TODO: add feature-selectors

    parser.add_argument('--classifiers',
                        required=True,
                        dest='classifiers',
                        type=valid_classifiers,
                        help='a list of classifiers to train. Possible choices [dt, logit, nb, rf, svm]')

    parser.add_argument('-d', '--destination',
                        required=True,
                        action='store',
                        dest='dest',
                        type=valid_dir,
                        help='destination folder to save the model and reports')

    """
    parser.add_argument('--verbose',
                        action='store_true',
                        dest='verbose',
                        default=False,
                        help='show log')
    """


def set_predict_parser(subparsers):
    parser = subparsers.add_parser('predict', help='Predict unseen instances')

    parser.add_argument('--path-to-model',
                        required=True,
                        action='store',
                        dest='path_to_model_dir',
                        type=valid_dir,
                        help='path to the folder containing the files related to the model')

    parser.add_argument('--path-to-file',
                        required=True,
                        action='store',
                        dest='path_to_file',
                        type=valid_file,
                        help='the path to the file to analyze')

    parser.add_argument('-l', '--language',
                        required=True,
                        action='store',
                        dest='language',
                        type=str,
                        choices=['ansible', 'tosca'],
                        help='the language of the file (i.e., TOSCA or YAML-based Ansible)')

    parser.add_argument('-d', '--destination',
                        required=True,
                        action='store',
                        dest='dest',
                        type=valid_dir,
                        help='destination folder to save the prediction report')


def set_download_model_parser(subparsers):
    parser = subparsers.add_parser('download', help='Download a pre-trained model from the online APIs')
    parser.add_argument('--path-to-repository',
                        required=True,
                        action='store',
                        dest='path_to_repository',
                        type=valid_dir,
                        help='path to the cloned repository')

    parser.add_argument('--host',
                        required=True,
                        action='store',
                        dest='host',
                        type=str,
                        choices=['github', 'gitlab'],
                        help='whether the repository is hosted on Github or Gitlab')

    parser.add_argument('-t', '--token',
                        required=False,  # TODO: handle with environment variable
                        action='store',
                        dest='token',
                        type=str,
                        help='the Github or Gitlab personal access token')

    parser.add_argument('-l', '--language',
                        required=True,
                        action='store',
                        dest='language',
                        type=str,
                        choices=['ansible', 'tosca'],
                        help='the language of the file (i.e., TOSCA or YAML-based Ansible)')

    parser.add_argument('-d', '--destination',
                        required=True,
                        action='store',
                        dest='dest',
                        type=valid_dir,
                        help='destination folder to save the model')


"""
def set_load_model_parser(subparsers):
    parser = subparsers.add_parser('load', help='Load a pre-trained model from the disk')
    parser.add_argument('--path-to-model',
                        required=True,
                        action='store',
                        dest='path_to_model_dir',
                        type=valid_dir,
                        help='path to the folder containing the model report')
"""


def set_model_parser(subparsers):
    parser = subparsers.add_parser('model', help='Get a pre-trained model to predict unseen instances')
    subparsers = parser.add_subparsers(dest='command')
    set_download_model_parser(subparsers)
    # set_load_model_parser(subparsers)


def get_parser():
    description = 'A Python library to train machine learning models for defect prediction of infrastructure code'

    parser = ArgumentParser(prog='radon-defect-predictor', description=description)
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.1.0')
    subparsers = parser.add_subparsers(dest='command')

    set_train_parser(subparsers)
    set_model_parser(subparsers)
    set_predict_parser(subparsers)

    return parser


def train(args: Namespace):
    dp = DefectPredictor()
    dp.balancers = args.balancers
    dp.normalizers = args.normalizers
    dp.classifiers = args.classifiers
    dp.train(pd.read_csv(args.path_to_csv))
    dp.dump_model(args.dest)
    exit(0)


def model(args: Namespace):
    print(args)
    exit(0)


def predict(args: Namespace):
    dp = DefectPredictor()
    dp.load_model(args.path_to_model_dir)

    # Read content of the script to analyze
    with open(args.path_to_file, 'r') as f:
        script_content = f.read()

    # Extract metrics
    if args.language == 'ansible':
        metrics = metrics_extractor.extract_all(io.StringIO(script_content))
    else:  # tosca
        metrics = {}  # use toscametrics

    unseen_data = pd.DataFrame(metrics, index=[0])
    prediction = dp.predict(unseen_data)
    report = dict(
        file=args.path_to_file,
        failure_prone=prediction,
        analyzed_at=str(datetime.date.today())
    )

    with open(os.path.join(args.dest, 'prediction_report.json'), 'a') as f:
        json.dump(report, f)

    exit(0)


def main():
    args = get_parser().parse_args()

    if args.command == 'train':
        train(args)
    elif args.command == 'model':
        model(args)
    elif args.command == 'predict':
        predict(args)
