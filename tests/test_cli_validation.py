import unittest

from argparse import ArgumentTypeError
from radondp.cli import valid_dir, valid_file, valid_balancers, valid_normalizers, valid_classifiers


class CLIValidationTestCase(unittest.TestCase):

    def test_valid_dir(self):
        with self.assertRaises(ArgumentTypeError):
            valid_dir('this/is/an/invalid/dir')

    def test_valid_file(self):
        with self.assertRaises(ArgumentTypeError):
            valid_file('this/is/an/invalid/file.yml')

    def test_valid_balancers(self):
        with self.assertRaises(ArgumentTypeError):
            valid_balancers('none ros rus invalid')

    def test_valid_normalizers(self):
        with self.assertRaises(ArgumentTypeError):
            valid_normalizers('none std minmax invalid')

    def test_valid_classifiers(self):
        with self.assertRaises(ArgumentTypeError):
            valid_classifiers('dt logit nb rf svm invalid')


if __name__ == '__main__':
    unittest.main()
