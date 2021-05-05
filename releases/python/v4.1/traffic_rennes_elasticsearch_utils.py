# coding: utf-8

import json
import time

import requests
from elasticsearch import Elasticsearch
from flask import flash

global message, es


class Config():
    def __init__(self):
        self.index_name = "traffic_rennes"
        self.index_init = False
        self.traffic_nb_rows = 10
        self.traffic_reliability = 5
        self.traffic_time_interval = 5
        self.traffic_time_max = 15


def read_json():
    jsonFile = "param.json"
    try:
        with open(jsonFile) as f:
            file_data = json.load(f)
            f.close()
    except:
        file_data = Config.query.all()
        submission_successful = "could not read file"

    return file_data


### Connection elastic search
# test le port elasticsearch
def connect_elasticsearch():
    es = None
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    if es.ping():
        flash('--> elasticsearch bien connecté')
    else:
        flash('--> /!\ elasticSearch pas de réponse')
    return es


# flash le contenu d'un json
def jflash(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)


def test():
    flash('--> test flash')


# demarrage
def loadData():
    param = read_json()
    # url
    traffic_url = "https://data.rennesmetropole.fr/api/records/1.0/search/?dataset=etat-du-trafic-en-temps-reel&q=&rows=" + str(
        param.traffic_nb_rows)

    flash("\n- Api traffic:")
    flash("\n--> url:", traffic_url)
    flash("\n--> nombre de lignes à prendre:", param.traffic_nb_rows)
    flash("\n--> reliability: >={}%".format(param.traffic_reliability))
    flash(
        "\n--> rafraichissement: tous les {}s (max de {}s)".format(param.traffic_time_interval, param.traffic_time_max))
    flash("\n\n- Elasticsearch index:", param.index_name)

    # %% ### Connection elastic search
    time.sleep(1)
    flash("\n\nConnection à elasticsearch")
    # crée une connection elasticsearch
    es = connect_elasticsearch()

    # ### Initialisation de l'index et mapping
    time.sleep(1)
    flash(f"\n\nGestion de l'index '{param.index_name}'")

    index_create = False
    if param.index_init:
        index_create = True
        if es.indices.exists(index=param.index_name):
            index_init_text = "remplacement (après suppression)"
            es.indices.delete(index=param.index_name)
        else:
            index_init_text = "création"
    else:
        if es.indices.exists(index=param.index_name):
            index_init_text = "mise à jour"
        else:
            index_create = True
            index_init_text = "création (car index non existant pour maj)"

    flash("--> opéation à réaliser sur l'index:", index_init_text)

    # mappings pour les coordonnées geospatiales
    req_body = {
        "mappings": {
            "properties": {
                "fields": {
                    "properties": {
                        # fields.geo_point_2d
                        "geo_point_2d": {"type": "geo_point"},

                        # fields.geo_shape
                        "geo_shape": {"type": "geo_shape"}
                    }
                },

                "geometry": {
                    "properties": {
                        # geometry.coordinates
                        "coordinates": {"type": "geo_point"}
                    }
                }
            }
        }
    }

    # crée l'índex vide
    if index_create:
        es.indices.create(index=param.index_name, body=req_body)
        flash("--> index bien créé!")

    nb_rows_elastic1 = es.count(index=param.index_name)["count"]
    flash("--> nombre de documents dans l'index:", nb_rows_elastic1)

    # %% ### Loop
    time.sleep(1)
    flash("\n\nApi traffic to Elasticsearch: stream-processing")
    traffic_nb_requete = int(param.traffic_time_max / param.traffic_time_interval)
    flash(f"- stream-config: il y aura {traffic_nb_requete} requêtes à faire tous les {param.traffic_time_interval}s")

    flash("- stream-starts:", time.strftime("%Y/%m/%d %H:%M:%S"))
    cpt = 1
    while cpt <= traffic_nb_requete:
        flash(f"\n--- Requête {cpt}/{traffic_nb_requete} ---")
        flash("- lancement:", time.strftime("%Y/%m/%d %H:%M:%S"))

        ### Import depuis l'api traffic
        flash("\n- API traffic")

        # get
        traffic = requests.get(traffic_url)
        if traffic.status_code == 200:
            flash("--> requête ok!")
        else:
            flash("--> requête non-ok!")
            flash("----> erreur :", traffic.status_code)

        # les données
        data_json = traffic.json()
        data = data_json["records"]
        nb_rows1 = len(data)
        flash(f"--> nombre de documents importés: {nb_rows1}/{param.traffic_nb_rows}")

        ### Data processing
        flash("\n- Qualité des données")

        flash("--> reliability...")
        data = [i for i in data if i["fields"]["traveltimereliability"] >= param.traffic_reliability]

        nb_rows2 = len(data)
        nb_rows3 = nb_rows1 - nb_rows2
        flash(f"----> nombre de documents restants: {nb_rows2}/{nb_rows1} ({nb_rows3} supprimés)")

        ### Export vers elasticsearch
        flash("\n- Export vers elasticsearch")

        # export vers elastic
        flash("--> export en cours...")
        i = es.count(index=param.index_name)['count'] + 1
        j = 0
        for doc_body in data:
            req = es.index(index=param.index_name, id=i, doc_type='_doc', body=doc_body)
            i = i + 1
            j = j + 1
        flash(f"----> nombre de documents exportés: {j}/{nb_rows2}")

        ### attente / rafraichissement
        if cpt < traffic_nb_requete:
            flash(f"\n(--- attente-de-{param.traffic_time_interval}s-avant-nouvel-appel-api ---)\n")
            time.sleep(param.traffic_time_interval)
        cpt = cpt + 1

    nb_rows_elastic2 = es.count(index=param.index_name)["count"]
    flash("\n- stream-ends:", time.strftime("%Y/%m/%d %H:%M:%S"))
    # %% check elasticsearch
    time.sleep(3)
    flash("\n\nElasticsearch")
    nb_rows_elastic2 = es.count(index=param.index_name)["count"]
    flash(f"--> nombre total de documents dans l'index: {nb_rows_elastic2}/{param.nb_rows_elastic1}")
    flash("\n\nFin-programme-python:", time.strftime("%Y/%m/%d %H:%M:%S"), "\n")
