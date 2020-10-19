import unittest
import os
import shutil


class CLITestCase(unittest.TestCase):
    test_model_folder = None

    @classmethod
    def setUpClass(cls):
        cls.test_model_folder = os.path.join(os.getcwd(), 'test_data', 'model')
        cls.test_trained_model_folder = os.path.join(os.getcwd(), 'test_data', 'trained_model')
        os.mkdir(cls.test_model_folder)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.test_model_folder)

    def test_train(self):
        command = """radon-defect-predictor train --path-to-csv {0} --balancers "none rus ros" \
                  --normalizers "none minmax std" --classifiers "nb" --destination {1} \
                  """.format(os.path.join(os.getcwd(), "test_data", "train_set.csv"), self.test_model_folder)

        print(command)
        result = os.system(command)

        assert (0 == result)
        assert os.path.isfile(os.path.join(self.test_model_folder, 'model.pkl'))
        assert os.path.isfile(os.path.join(self.test_model_folder, 'model_features.json'))
        assert os.path.isfile(os.path.join(self.test_model_folder, 'model_report.json'))

    def test_model(self):
        pass

    def test_predict(self):
        command = """
        radon-defect-predictor predict --path-to-model {0} --path-to-file {1} -l ansible --d {2}
        """.format(self.test_trained_model_folder,
                   os.path.join(os.getcwd(), "test_data", "an_ansible_playbook.yml"),
                   self.test_model_folder)

        result = os.system(command)

        assert (0 == result)
        assert os.path.isfile(os.path.join(self.test_model_folder, 'prediction_report.json'))


if __name__ == '__main__':
    unittest.main()
