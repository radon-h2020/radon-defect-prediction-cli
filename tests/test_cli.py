import unittest
import os
import shutil

from dotenv import load_dotenv


class CLITestCase(unittest.TestCase):
    test_model_folder = None
    test_download_model_folder = None

    @classmethod
    def setUpClass(cls):
        cls.test_repositories = os.path.join(os.getcwd(), 'test_data', 'repositories')
        cls.test_trained_model_folder = os.path.join(os.getcwd(), 'test_data', 'trained_model')

        cls.test_model_folder = os.path.join(os.getcwd(), 'test_data', 'model')
        os.mkdir(cls.test_model_folder)

        cls.test_download_model_folder = os.path.join(os.getcwd(), 'test_data', 'download_model')
        os.mkdir(cls.test_download_model_folder)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.test_download_model_folder)
        shutil.rmtree(cls.test_model_folder)

    def test_model(self):
        load_dotenv()
        access_token = os.getenv('GITHUB_ACCESS_TOKEN')
        print(access_token)

        command = """
        radon-defect-predictor model download --path-to-repository {0} --host github -t {1} -o ANXS -n postgresql -l ansible -d {2}
        """.format(os.path.join(self.test_repositories, 'postgresql'),
                   access_token,
                   self.test_download_model_folder)

        result = os.system(command)

        assert (0 == result)
        assert os.path.isfile(os.path.join(self.test_download_model_folder, 'model.pkl'))
        assert os.path.isfile(os.path.join(self.test_download_model_folder, 'model_features.json'))


if __name__ == '__main__':
    unittest.main()
