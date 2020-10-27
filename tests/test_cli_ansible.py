import joblib
import json
import os
import shutil
import unittest


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
        cls.downloaded_model_dir = os.path.join(cls.workdir, 'downloaded_model')
        cls.predict_dir = os.path.join(cls.workdir, 'predict')

        os.mkdir(cls.workdir)
        os.mkdir(cls.train_dir)
        os.mkdir(cls.downloaded_model_dir)
        os.mkdir(cls.predict_dir)

        os.system('cp {0} {1}/radondp_model.joblib'.format(
            os.path.join(os.getcwd(), "test_data", "radondp_model_ansible.joblib"),
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
        command = 'cd {0} && radon-defect-predictor download-model ansible github ANXS/postgresql {1}'.format(self.downloaded_model_dir,
                                                                                                              self.repository)
        result = os.system(command)
        assert (0 == result)

        model = joblib.load(os.path.join(self.downloaded_model_dir, 'radondp_model.joblib'), mmap_mode='r')
        assert model['model']
        assert model['features']


    def test_predict(self):
        command = 'cd {0} && radon-defect-predictor predict ansible {1}'.format(self.predict_dir, self.playbook)
        result = os.system(command)

        assert (0 == result)

        with open(os.path.join(self.predict_dir, 'radondp_predictions.json'), 'r') as f:
            predictions = json.load(f)
            assert len(predictions) == 1
            assert predictions[0]['file'] == self.playbook
            assert type(predictions[0]['failure_prone']) == bool


if __name__ == '__main__':
    unittest.main()
