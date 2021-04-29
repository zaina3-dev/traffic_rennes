import unittest
import pathlib
import requests
from elasticsearch import Elasticsearch


class TestConfiguration(unittest.TestCase):

    # avant les tests
    def setUp(self):
        self.name_file = "traffic_rennes_parameters.txt"
        self.params_sep = " = "
        self.traffic_url = "https://data.rennesmetropole.fr/api/records/1.0/search/?dataset=etat-du-trafic-en-temps-reel"

    # vérifie la présence fichier de configuration
    def test_check_file(self):
        path = pathlib.Path(self.name_file)
        if not path.resolve().is_file():
            raise AssertionError("File does not exist: %s" % str(path))


    # vérifie les paramétres de configuration
    def test_check_param(self):
        fichier = open(file=self.name_file, mode="r", newline="")
        params_list = [line.rstrip() for line in fichier.readlines() if (line[0] != '#' and self.params_sep in line)]
        fichier.close()

        self.params = {}
        for i in params_list:
            a = i.split(self.params_sep)
            self.params[a[0]] = a[1]
        # print(self.params["traffic_nb_rows"])
        self.assertTrue(type(str(self.params["index_name"])) is str)
        self.assertTrue(type(bool(self.params["index_init"])) is bool)
        self.assertTrue(type(int(self.params["traffic_nb_rows"])) is int)
        self.assertTrue(type(int(self.params["traffic_reliability"])) is int)
        self.assertTrue(type(int(self.params["traffic_time_interval"])) is int)
        self.assertTrue(type(int(self.params["traffic_time_max"])) is int)

    # vérifie la réponse de l'api url
    def test_api(self):
        response = requests.get(self.traffic_url)
        self.assertEqual(200, response.status_code)

    # vérifie le port d'elasticsearch
    def test_elastic(self):
        self.assertTrue(Elasticsearch([{'host': 'localhost', 'port': 9200}]))


if __name__ == '__main__':
    unittest.main()
