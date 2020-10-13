import argparse
import os
import pandas as pd
from .train import DefectPredictor


def valid_dir(x: str) -> str:
    """
    Check the directory exists
    :param x: a path
    :return: the path if exists; raise an ArgumentTypeError otherwise
    """
    if not os.path.isdir(x):
        raise argparse.ArgumentTypeError('Insert a valid path')

    return x

def valid_file(x: str) -> str:
    """
    Check the file exists
    :param x: a path
    :return: the path if exists; raise an ArgumentTypeError otherwise
    """
    if not os.path.isfile(x):
        raise argparse.ArgumentTypeError('Insert a valid path')

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
            raise argparse.ArgumentTypeError(f'{balancer} is not a valid argument')

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
            raise argparse.ArgumentTypeError(f'{normalizer} is not a valid argument')

    return normalizers


def valid_classifiers(x: str):
    """
    Check x is a list of valid classifiers
    :param x: a string representing a list of classifiers (e.g., "decision-tree logistic-regression naive-bayes random-forest svm")
    :return: the list of classifiers if every argument in x is a valid classifier; raise an ArgumentTypeError otherwise
    """
    classifiers = x.split(' ')
    for classifier in classifiers:
        if classifier not in ('decision-tree', 'logistic-regression', 'naive-bayes', 'random-forest', 'svm'):
            raise argparse.ArgumentTypeError(f'{classifier} is not a valid argument')

    return classifiers


def get_parser():
    description = 'A Python library to train machine learning models for defect prediction of infrastructure code.'

    parser = argparse.ArgumentParser(prog='radon-defect-predictor', description=description)
    parser.add_argument('-v', '--version', action='version', version='%(prog)s')

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

    parser.add_argument('--classifiers',
                        required=True,
                        dest='classifiers',
                        type=valid_classifiers,
                        help='a list of classifiers to train. Possible choices [decision-tree, logistic-regression, '
                             'naive-bayes, random-forest, svm]')

    parser.add_argument('-d', '--destination',
                        required=True,
                        action='store',
                        dest='dest',
                        type=valid_dir,
                        help='destination folder to save model reports')

    """
    parser.add_argument('--verbose',
                        action='store_true',
                        dest='verbose',
                        default=False,
                        help='show log')
    """
    return parser


def main():
    args = get_parser().parse_args()

    dp = DefectPredictor(
        data=pd.read_csv(args.path_to_csv),
        classifiers=args.classifiers,
        balancers=args.balancers if args.balancers else [],
        normalizers=args.normalizers if args.normalizers else []
    )

    dp.train()
