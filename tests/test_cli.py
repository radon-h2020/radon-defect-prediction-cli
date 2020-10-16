import unittest
import os
import shutil


class CLITestCase(unittest.TestCase):
    test_model_folder = None

    @classmethod
    def setUpClass(cls) -> None:
        # Install command
        os.system('pip install .')
        cls.test_model_folder = os.path.join(os.getcwd(), 'test_data', 'model')
        cls.test_trained_model_folder = os.path.join(os.getcwd(), 'test_data', 'trained_model')
        os.mkdir(cls.test_model_folder)

    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree(cls.test_model_folder)

    def test_train(self):
        result = os.system(
            f'radon-defect-predictor train --path-to-csv {os.path.join(os.getcwd(), "test_data", "train_set.csv")} '
            f'--balancers "none rus ros" --normalizers "none minmax std" --classifiers "nb" '
            f'--destination {self.test_model_folder}')

        assert (0 == result)
        assert os.path.isfile(os.path.join(self.test_model_folder, 'model.pkl'))
        assert os.path.isfile(os.path.join(self.test_model_folder, 'model_features.json'))
        assert os.path.isfile(os.path.join(self.test_model_folder, 'model_report.json'))

    def test_model(self):
        pass

    def test_predict(self):
        result = os.system(f'radon-defect-predictor predict --path-to-model {self.test_trained_model_folder} '
                           f'--path-to-file {os.path.join(os.getcwd(), "test_data", "an_ansible_playbook.yml")} '
                           f'-l ansible --destination {self.test_model_folder}')

        assert (0 == result)
        assert os.path.isfile(os.path.join(self.test_model_folder, 'prediction_report.json'))

if __name__ == '__main__':
    unittest.main()
