import unittest
import pathlib
import requests
from elasticsearch import Elasticsearch


class TestConfiguration(unittest.TestCase):

    # avant les tests
    def setUp(self):
        self.utils_file = 'trafficrennes_transfertdata_utils.py'
        self.params_file = 'trafficrennes_transfertdata_parameters.txt'
        self.params_sep = ' = '

        self.traffic_url = 'https://data.rennesmetropole.fr/api/records/1.0/search/?dataset=etat-du-trafic-en-temps-reel'

        self.es_host = 'localhost'
        self.es_port = 9200


    # vérifie la présence fichier de configuration
    def test_check_file(self):
        # utils file
        path = pathlib.Path(self.utils_file)
        if not path.resolve().is_file():
            raise AssertionError('File does not exist: %s' % str(path))
        
        # parameters file
        path = pathlib.Path(self.params_file)
        if not path.resolve().is_file():
            raise AssertionError('File does not exist: %s' % str(path))


    # vérifie les paramétres de configuration
    def test_check_param(self):
        fichier = open(file=self.params_file, mode='r', newline='')
        params_list = [line.rstrip() for line in fichier.readlines() if (line[0] != '#' and self.params_sep in line)]
        fichier.close()

        self.params = {}
        for i in params_list:
            j = i.split(self.params_sep)
            self.params[j[0]] = j[1]
        
        # type
        self.assertTrue(type(str(self.params['index_name'])) is str)
        self.assertTrue(self.params['index_init'] in ['True','False'])        
        self.assertTrue(type(int(self.params['traffic_nb_rows'])) is int)
        self.assertTrue(type(int(self.params['traffic_reliability'])) is int)
        self.assertTrue(type(int(eval(self.params['traffic_time_interval']))) is int)
        self.assertTrue(type(int(eval(self.params['traffic_time_max']))) is int)
        
        # cohérence valeurs
        self.assertTrue(int(eval(self.params['traffic_time_max'])) >= int(eval(self.params['traffic_time_interval'])))


    # vérifie la réponse de l'api url
    def test_api(self):
        response = requests.get(self.traffic_url)
        self.assertEqual(200, response.status_code)


    # vérifie le port d'elasticsearch
    def test_elastic(self):
        es = Elasticsearch([{'host':self.es_host, 'port':self.es_port}])
        es_server = self.es_host +':'+ str(self.es_port) +'/'
        if not es.ping():
            raise AssertionError('Elasticsearch server not connected: %s' % str(es_server))


if __name__ == '__main__':
    unittest.main()
