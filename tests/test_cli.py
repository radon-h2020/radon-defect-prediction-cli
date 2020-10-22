import unittest
import os
import shutil

from dotenv import load_dotenv


class CLITestCase(unittest.TestCase):
    path_to_new_ansible_model = None
    path_to_new_tosca_model = None
    path_to_download_model = None

    @classmethod
    def setUpClass(cls):
        load_dotenv()

        cls.test_repositories = os.path.join(os.getcwd(), 'test_data', 'repositories')
        cls.path_to_trained_ansible_model = os.path.join(os.getcwd(), 'test_data', 'trained_model_ansible')
        cls.path_to_trained_tosca_model = os.path.join(os.getcwd(), 'test_data', 'trained_model_tosca')

        cls.path_to_new_ansible_model = os.path.join(os.getcwd(), 'test_data', 'model_ansible')
        os.mkdir(cls.path_to_new_ansible_model)

        cls.path_to_new_tosca_model = os.path.join(os.getcwd(), 'test_data', 'model_tosca')
        os.mkdir(cls.path_to_new_tosca_model)

        cls.path_to_download_model = os.path.join(os.getcwd(), 'test_data', 'download_model')
        os.mkdir(cls.path_to_download_model)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.path_to_download_model)
        shutil.rmtree(cls.path_to_new_ansible_model)
        shutil.rmtree(cls.path_to_new_tosca_model)

    def test_train_ansible(self):
        command = """radon-defect-predictor train --path-to-csv {0} --balancers "none rus ros" \
                  --normalizers "none minmax std" --classifiers "nb" --destination {1} \
                  """.format(os.path.join(os.getcwd(), "test_data", "ansible_train_set.csv"),
                             self.path_to_new_ansible_model)

        result = os.system(command)

        assert (0 == result)
        assert os.path.isfile(os.path.join(self.path_to_new_ansible_model, 'model.pkl'))
        assert os.path.isfile(os.path.join(self.path_to_new_ansible_model, 'model_features.json'))
        assert os.path.isfile(os.path.join(self.path_to_new_ansible_model, 'model_report.json'))

    def test_train_tosca(self):
        command = """radon-defect-predictor train --path-to-csv {0} --balancers "none rus ros" \
                  --normalizers "none minmax std" --classifiers "dt" --destination {1} \
                  """.format(os.path.join(os.getcwd(), "test_data", "tosca_train_set.csv"),
                             self.path_to_new_tosca_model)

        result = os.system(command)

        assert (0 == result)
        assert os.path.isfile(os.path.join(self.path_to_new_tosca_model, 'model.pkl'))
        assert os.path.isfile(os.path.join(self.path_to_new_tosca_model, 'model_features.json'))
        assert os.path.isfile(os.path.join(self.path_to_new_tosca_model, 'model_report.json'))

    def test_model(self):
        command = """
        radon-defect-predictor model download --path-to-repository {0} --host github -t {1} -r ANXS/postgresql -l ansible -d {2}
        """.format(os.path.join(self.test_repositories, 'postgresql'),
                   os.getenv('GITHUB_ACCESS_TOKEN'),
                   self.path_to_download_model)

        result = os.system(command)

        assert (0 == result)
        assert os.path.isfile(os.path.join(self.path_to_download_model, 'model.pkl'))
        assert os.path.isfile(os.path.join(self.path_to_download_model, 'model_features.json'))

    def test_predict_ansible(self):
        command = """
        radon-defect-predictor predict --path-to-model {0} --path-to-file {1} -l ansible --d {2}
        """.format(self.path_to_trained_ansible_model,
                   os.path.join(os.getcwd(), "test_data", "an_ansible_playbook.yml"),
                   self.path_to_new_ansible_model)

        result = os.system(command)

        assert (0 == result)
        assert os.path.isfile(os.path.join(self.path_to_new_ansible_model, 'prediction_report.json'))

    def test_predict_tosca(self):
        command = """
        radon-defect-predictor predict --path-to-model {0} --path-to-file {1} -l tosca --d {2}
        """.format(self.path_to_trained_tosca_model,
                   os.path.join(os.getcwd(), "test_data", "a_tosca_definition.tosca"),
                   self.path_to_new_tosca_model)

        result = os.system(command)

        assert (0 == result)
        assert os.path.isfile(os.path.join(self.path_to_new_tosca_model, 'prediction_report.json'))


if __name__ == '__main__':
    unittest.main()
