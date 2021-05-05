import json
import subprocess
import os
import time

from flask import Flask, render_template, request, flash, jsonify
import pathlib
import requests

# App config
# from test.traffic_rennes_elasticsearch_utils import jprint
from traffic_rennes_elasticsearch_utils import connect_elasticsearch, read_json, Config, loadData, test

DEBUG = True
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

jsonFile = "param.json"


@app.route('/_stuff/<task>', methods=['GET'])
def stuff(task):
    param = read_json()
    # flash('You were successfully logged in!!!!!!!!!!')
    # connect to elasticsearch
    if task == 'elastic':
        result = connect_elasticsearch()
        # print(result.ping())
        flash('elastic ==')
        return jsonify(result.ping())
        # send message with param default
    if task == 'resume':
        loadData()
        flash('resume ==')
        return jsonify("load data")

    if task == 'test':
        test()
        flash('test ==')
        return jsonify("test")

    #  index create or update
    if task == 'index':
        if (param.index_init):
            result = connect_elasticsearch()
            print(result.ping())
            return jsonify(result.ping())


@app.route("/", methods=["GET", "POST"])
def results():
    title = "Tests"
    file_data = ""
    submission_successful = False
    if request.method == "POST":
        print(request.form)
        with open(jsonFile, "w+") as f:
            json.dump(request.form, f)
        submission_successful = True
        flash('You were successfully logged in')

    #  filepath = ".run_traffic_elasticsearch.bat"
    #  p = subprocess.Popen(filepath, shell=True, stdout=subprocess.PIPE)
    #  stdout, stderr = p.communicate()
    #  print(p.returncode)  # is 0 if success

    try:
        with open(jsonFile) as f:
            file_data = json.load(f)
            f.close()
            flash('Config default')
            flash('Done')
    except:
        file_data = Config.query.all()
        submission_successful = "could not read file"

    return render_template('index.html', data=file_data, submission=submission_successful)

@app.route("/test", methods=["GET", "POST"])
def loadData():
    param = read_json()
    print("== param :", param['traffic_nb_rows'])
    # url
    traffic_url = "https://data.rennesmetropole.fr/api/records/1.0/search/?dataset=etat-du-trafic-en-temps-reel&q=&rows=" + str(
        param["traffic_nb_rows"])

    flash("\n- Api traffic:")
    flash("\n--> url:" + str(traffic_url))
    flash("\n--> nombre de lignes à prendre:" + str(param["traffic_nb_rows"]))
    flash("\n--> reliability: >=" + str(format(param["traffic_reliability"])))
    flash(
        "\n--> rafraichissement: tous les {}s (max de {}s)".format(param["traffic_time_interval"],
                                                                   param["traffic_time_max"]))
    flash("\n\n- Elasticsearch index:", param["index_name"])

    # %% ### Connection elastic search
    time.sleep(1)
    flash("\n\nConnection à elasticsearch")
    # crée une connection elasticsearch
    es = connect_elasticsearch()

    # ### Initialisation de l'index et mapping
    time.sleep(1)
    flash(f"\n\nGestion de l'index '{param['index_name']}'")

    index_create = False
    print("== param init :", param)
    print("== param init :", param['index_init'])
    if param["index_init"]:
        index_create = True
        if es.indices.exists(index=param["index_name"]):
            index_init_text = "remplacement (après suppression)"
            es.indices.delete(index=param["index_name"])
        else:
            index_init_text = "création"
    else:
        if es.indices.exists(index=param["index_name"]):
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
        es.indices.create(index=param["index_name"], body=req_body)
        flash("--> index bien créé!")

    nb_rows_elastic1 = es.count(index=param["index_name"])["count"]
    flash("--> nombre de documents dans l'index:", nb_rows_elastic1)

    # %% ### Loop
    time.sleep(1)
    flash("\n\nApi traffic to Elasticsearch: stream-processing")
    traffic_nb_requete = int(param["traffic_time_max"] / param['traffic_time_interval'])
    flash(
        f"- stream-config: il y aura {traffic_nb_requete} requêtes à faire tous les {param['traffic_time_interval']}s")

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
        flash(f"--> nombre de documents importés: {nb_rows1}/{param['traffic_nb_rows']}")

        ### Data processing
        flash("\n- Qualité des données")

        flash("--> reliability...")
        data = [i for i in data if i["fields"]["traveltimereliability"] >= param["traffic_reliability"]]

        nb_rows2 = len(data)
        nb_rows3 = nb_rows1 - nb_rows2
        flash(f"----> nombre de documents restants: {nb_rows2}/{nb_rows1} ({nb_rows3} supprimés)")

        ### Export vers elasticsearch
        flash("\n- Export vers elasticsearch")

        # export vers elastic
        flash("--> export en cours...")
        i = es.count(index=param["index_name"])['count'] + 1
        j = 0
        for doc_body in data:
            req = es.index(index=param["index_name"], id=i, doc_type='_doc', body=doc_body)
            i = i + 1
            j = j + 1
        flash(f"----> nombre de documents exportés: {j}/{nb_rows2}")

        ### attente / rafraichissement
        if cpt < traffic_nb_requete:
            flash(f"\n(--- attente-de-{param['traffic_time_interval']}s-avant-nouvel-appel-api ---)\n")
            time.sleep(param["traffic_time_interval"])
        cpt = cpt + 1
    nb_rows_elastic2 = es.count(index=param["index_name"])["count"]
    flash("\n- stream-ends:", time.strftime("%Y/%m/%d %H:%M:%S"))
    # %% check elasticsearch
    time.sleep(3)
    flash("\n\nElasticsearch")
    nb_rows_elastic2 = es.count(index=param["index_name"])["count"]
    flash(f"--> nombre total de documents dans l'index: {nb_rows_elastic2}/{nb_rows_elastic1}")
    # flash("\n\nFin-programme-python:", time.strftime("%Y/%m/%d %H:%M:%S"), "\n")
    return render_template('statut.html')

if __name__ == "__main__":
    app.run()
