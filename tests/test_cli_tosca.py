import joblib
import json
import os
import shutil
import unittest

from dotenv import load_dotenv


class CLIToscaTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        load_dotenv()

        cls.training_data_csv = os.path.join(os.getcwd(), "test_data", "tosca.csv")
        cls.tosca_definition = os.path.join(os.getcwd(), "test_data/definition.tosca")
        cls.tosca_csar = os.path.join(os.getcwd(), "test_data/tosca.csar")

        # Create a working directory for Ansible
        cls.workdir = os.path.join(os.getcwd(), 'test_data', 'tosca_workdir')
        cls.train_dir = os.path.join(cls.workdir, 'train')
        cls.predict_dir = os.path.join(cls.workdir, 'predict')

        os.mkdir(cls.workdir)
        os.mkdir(cls.train_dir)
        os.mkdir(cls.predict_dir)

        os.system('cp {0} {1}/radondp_model.joblib'.format(
            os.path.join(os.getcwd(), "test_data", "radondp_model_tosca.joblib"),
            cls.predict_dir))

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.workdir)

    def test_train(self):
        command = """
        cd {0} && radon-defect-predictor train {1} "nb" -b "none rus ros" -n "none minmax std"
        """.format(self.train_dir, self.training_data_csv)

        result = os.system(command)

        assert (0 == result)
        assert 'radondp_model.joblib' in os.listdir(self.train_dir)
        model = joblib.load(os.path.join(self.train_dir, 'radondp_model.joblib'), mmap_mode='r')
        assert model['model']
        assert model['features']
        assert model['report']

    def test_model(self):
        pass

    def test_predict(self):
        command = 'cd {0} && radon-defect-predictor predict tosca {1}'.format(self.predict_dir, self.tosca_definition)
        result = os.system(command)

        assert (0 == result)

        with open(os.path.join(self.predict_dir, 'radondp_predictions.json'), 'r') as f:
            predictions = json.load(f)
            assert len(predictions) == 1
            assert predictions[0]['file'] == self.tosca_definition
            assert type(predictions[0]['failure_prone']) == bool

    def test_predict_tosca_csar(self):
        path_to_csar = os.path.join(os.getcwd(), "test_data", "tosca.csar")

        command = 'cd {0} && radon-defect-predictor predict tosca {1}'.format(self.predict_dir, self.tosca_csar)
        result = os.system(command)

        assert (0 == result)

        with open(os.path.join(self.predict_dir, 'radondp_predictions.json'), 'r') as f:
            predictions = json.load(f)

            files = set([item['file'] for item in predictions])
            assert os.path.join(self.tosca_csar, '_definitions/radonartifacts__Ansible.tosca') in files
            assert os.path.join(self.tosca_csar, '_definitions/radonnodesaws__AwsLambdaFunction.tosca') in files
            assert os.path.join(self.tosca_csar, '_definitions/radondatatypesfunction__Entries.tosca') in files


if __name__ == '__main__':
    unittest.main()
