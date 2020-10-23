import joblib
import os
import shutil
import unittest

from dotenv import load_dotenv


class CLIAnsibleTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        load_dotenv()

        # Path to training_data
        cls.training_data_csv = os.path.join(os.getcwd(), "test_data", "tosca_train_set.csv")

        # Create a working directory for Ansible
        cls.workdir = os.path.join(os.getcwd(), 'test_data', 'tosca_workdir')
        os.mkdir(cls.workdir)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.workdir)

    def test_train(self):
        command = """
        cd {0} && radon-defect-predictor train {1} "nb" -b "none rus ros" -n "none minmax std"
        """.format(self.workdir, self.training_data_csv)

        result = os.system(command)

        assert (0 == result)
        assert 'radondp_model.joblib' in os.listdir(self.workdir)
        model = joblib.load(os.path.join(self.workdir, 'radondp_model.joblib'), mmap_mode='r')
        assert model['model']
        assert model['features']
        assert model['report']


if __name__ == '__main__':
    unittest.main()
