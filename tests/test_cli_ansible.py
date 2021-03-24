import joblib
import json
import os
import shutil
import unittest

from argparse import Namespace
from radondp.cli import train, model as download_model, predict


class CLIAnsibleTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Path to training_data
        cls.training_data_csv = os.path.join(os.getcwd(), "test_data", "ansible.csv")
        cls.playbook = os.path.join(os.getcwd(), "test_data/playbook.yml")
        cls.repository = os.path.join(os.getcwd(), "test_data/repositories/postgresql")

        # Create a working directory for Ansible
        cls.workdir = os.path.join(os.getcwd(), 'test_data', 'ansible_workdir')
        cls.train_dir = os.path.join(cls.workdir, 'train')
        cls.download_model_dir = os.path.join(cls.workdir, 'downloaded_model')
        cls.predict_dir = os.path.join(cls.workdir, 'predict')

        os.mkdir(cls.workdir)
        os.mkdir(cls.train_dir)
        os.mkdir(cls.download_model_dir)
        os.mkdir(cls.predict_dir)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.workdir)

    def test_train_invalid_balancer(self):
        args = Namespace(
            balancers=['none', 'WRONG'],
            classifiers=['nb'],
            path_to_csv=self.training_data_csv
        )

        with self.assertRaises(ValueError):
            train(args)

    def test_train_invalid_normalizer(self):
        args = Namespace(
            normalizers=['none', 'WRONG'],
            classifiers=['nb'],
            path_to_csv=self.training_data_csv
        )

        with self.assertRaises(ValueError):
            train(args)

    def test_train_invalid_classifier(self):
        args = Namespace(
            classifiers=['WRONG'],
            path_to_csv=self.training_data_csv
        )

        with self.assertRaises(ValueError):
            train(args)

    def test_train_no_classifier(self):
        args = Namespace(
            path_to_csv=self.training_data_csv
        )

        with self.assertRaises(RuntimeError):
            train(args)

    def test_train(self):
        args = Namespace(
            balancers = ['none', 'rus', 'ros'],
            normalizers=['none', 'minmax', 'std'],
            classifiers=['nb'],
            path_to_csv=self.training_data_csv
        )

        try:
            train(args)
        except SystemExit as exc:
            assert exc.code == 0
            shutil.move('./radondp_model.joblib', os.path.join(self.train_dir, "radondp_model.joblib"))

            assert 'radondp_model.joblib' in os.listdir(self.train_dir)

            model = joblib.load(os.path.join(self.train_dir, 'radondp_model.joblib'), mmap_mode='r')
            assert model['estimator']
            assert model['selected_features']
            assert model['report']

    def test_download_model_no_language(self):
        args = Namespace()

        try:
            download_model(args)
        except SystemExit as exc:
            assert exc.code != 0

    def test_download_model_wrong_language(self):
        args = Namespace(language='wrong-language')

        try:
            download_model(args)
        except SystemExit as exc:
            assert exc.code != 0

    def test_download_model(self):
        args = Namespace(language='ansible')

        try:
            download_model(args)
        except SystemExit as exc:
            assert exc.code == 0
            shutil.move('./radondp_model.joblib', os.path.join(self.download_model_dir, "radondp_model.joblib"))

            model = joblib.load(os.path.join(self.download_model_dir, 'radondp_model.joblib'), mmap_mode='r')
            assert model['estimator']
            assert model['selected_features']

    def test_predict_no_language(self):
        args = Namespace(path_to_artefact=self.playbook)

        try:
            predict(args)
        except SystemExit as exc:
            assert exc.code != 0

    def test_predict_wrong_language(self):
        args = Namespace(language='wrong-language', path_to_artefact=self.playbook)

        try:
            predict(args)
        except SystemExit as exc:
            assert exc.code != 0

    def test_predict_no_artefact_path(self):
        args = Namespace(language='ansible')

        try:
            predict(args)
        except SystemExit as exc:
            assert exc.code != 0

    def test_predict(self):
        args = Namespace(language='ansible', path_to_artefact=self.playbook)

        try:
            shutil.copy(os.path.join(os.getcwd(), "test_data", "radondp_model_ansible.joblib"),
                        os.path.join(os.getcwd(), 'radondp_model.joblib'))

            predict(args)
        except SystemExit as exc:

            assert exc.code == 0

            shutil.move(os.path.join(os.getcwd(), 'radondp_model.joblib'),
                        os.path.join( self.predict_dir, 'radondp_model_ansible.joblib'))

            shutil.move(os.path.join(os.getcwd(), 'radondp_predictions.json'),
                        os.path.join( self.predict_dir, 'radondp_predictions.json'))

            with open(os.path.join(self.predict_dir, 'radondp_predictions.json'), 'r') as f:
                predictions = json.load(f)
                assert len(predictions) == 1
                assert predictions[0]['file'] == self.playbook
                assert type(predictions[0]['failure_prone']) == bool

if __name__ == '__main__':
    unittest.main()
