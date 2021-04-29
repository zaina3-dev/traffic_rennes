import unittest
import time
import sys
import utils
import pathlib


# import traffic_rennes_elasticsearch


class TestConfiguration(unittest.TestCase):

    # avant les tests
    def setUp(self):
        self.name_file = "traffic_rennes_parameters.txt"

    # présence fichier de configuration
    def test_check_file(self):
        path = pathlib.Path(self.name_file)
        if not path.resolve().is_file():
            raise AssertionError("File does not exist: %s" % str(path))

    # vérifie les paramétres de configuration


def test_check_param(self):
    fichier = open(file=self.name_file, mode="r", newline="")
    params_list = [line.rstrip() for line in fichier.readlines() if (line[0] != '#' and params_sep in line)]
    fichier.close()

    params = {}
    for i in params_list:
        a = i.split(params_sep)
        params[a[0]] = a[1]

def test_api(self):


if __name__ == '__main__':
    unittest.main()
