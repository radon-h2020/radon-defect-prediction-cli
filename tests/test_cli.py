import unittest
import json
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
        radon-defect-predictor predict --path-to-model {0} --path-to-artefact {1} -l ansible --d {2}
        """.format(self.path_to_trained_ansible_model,
                   os.path.join(os.getcwd(), "test_data", "an_ansible_playbook.yml"),
                   self.path_to_new_ansible_model)

        result = os.system(command)

        assert (0 == result)
        assert os.path.isfile(os.path.join(self.path_to_new_ansible_model, 'prediction_report.json'))

    def test_predict_tosca(self):
        command = """
        radon-defect-predictor predict --path-to-model {0} --path-to-artefact {1} -l tosca --d {2}
        """.format(self.path_to_trained_tosca_model,
                   os.path.join(os.getcwd(), "test_data", "a_tosca_definition.tosca"),
                   self.path_to_new_tosca_model)

        result = os.system(command)

        assert (0 == result)
        assert os.path.isfile(os.path.join(self.path_to_new_tosca_model, 'prediction_report.json'))

    def test_predict_tosca_csar(self):
        path_to_csar = os.path.join(os.getcwd(), "test_data", "tosca.csar")
        command = """
        radon-defect-predictor predict --path-to-model {0} --path-to-artefact {1} -l tosca --d {2}
        """.format(self.path_to_trained_tosca_model,
                   path_to_csar,
                   self.path_to_new_tosca_model)

        result = os.system(command)

        assert (0 == result)
        assert os.path.isfile(os.path.join(self.path_to_new_tosca_model, 'prediction_report.json'))

        with open(os.path.join(self.path_to_new_tosca_model, 'prediction_report.json'), 'r') as f:
            predictions = json.load(f)

        files = set([item['file'] for item in predictions])
        assert os.path.join(path_to_csar, '_definitions/tyIgeneral__Precedence.tosca') in files
        assert os.path.join(path_to_csar, '_definitions/radonnodesabstract__ApiGateway.tosca') in files
        assert os.path.join(path_to_csar, '_definitions/radonrelationshipsabstract__Triggers.tosca') in files
        assert os.path.join(path_to_csar, '_definitions/radonrelationshipsaws__ApiGatewayTriggers.tosca') in files
        assert os.path.join(path_to_csar, '_definitions/radonnodesabstract__Function.tosca') in files
        assert os.path.join(path_to_csar, '_definitions/tyIgeneral__RandomVariable.tosca') in files
        assert os.path.join(path_to_csar, '_definitions/radonnodesaws__AwsS3Bucket.tosca') in files
        assert os.path.join(path_to_csar, '_definitions/radonnodesaws__AwsPlatform.tosca') in files
        assert os.path.join(path_to_csar, '_definitions/radonrelationshipsaws__AwsTriggers.tosca') in files
        assert os.path.join(path_to_csar, '_definitions/tyIgeneral__Event.tosca') in files
        assert os.path.join(path_to_csar, '_definitions/radonnodesaws__AwsLambdaFunctionFromS3.tosca') in files
        assert os.path.join(path_to_csar, '_definitions/radonartifactsarchive__Zip.tosca') in files
        assert os.path.join(path_to_csar, '_definitions/radonnodesaws__AwsDynamoDBTable.tosca') in files
        assert os.path.join(path_to_csar, '_definitions/radonnodesaws__AwsLambdaFunction.tosca') in files
        assert os.path.join(path_to_csar, '_definitions/radondatatypesfunction__Entries.tosca') in files
        assert os.path.join(path_to_csar, '_definitions/tyIgeneral__Interaction.tosca') in files
        assert os.path.join(path_to_csar, '_definitions/radonnodesabstract__ObjectStorage.tosca') in files
        assert os.path.join(path_to_csar, '_definitions/radonnodesaws__AwsApiGateway.tosca') in files
        assert os.path.join(path_to_csar, '_definitions/radonrelationships__ConnectsTo.tosca') in files
        assert os.path.join(path_to_csar, '_definitions/tyIgeneral__Activity.tosca') in files
        assert os.path.join(path_to_csar, '_definitions/tyIgeneral__Entry.tosca') in files
        assert os.path.join(path_to_csar, '_definitions/radonartifacts__Ansible.tosca') in files
        assert os.path.join(path_to_csar, '_definitions/radonnodesVM__EC2.tosca') in files
        assert os.path.join(path_to_csar, '_definitions/radonnodesabstract__CloudPlatform.tosca') in files
        assert os.path.join(path_to_csar, '_definitions/steIgeneral__cloudstash_no_sourceCode_VT_version.tosca') in files
        assert os.path.join(path_to_csar, '_definitions/radoncapabilities__Invocable.tosca') in files


if __name__ == '__main__':
    unittest.main()
