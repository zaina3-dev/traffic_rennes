#!/usr/bin/env python
# coding: utf-8

# librairies
import time
import requests
import json

import utils



# ### Initialisation
time.sleep(1)
print("\nDébut:", time.strftime("%Y/%m/%d %H:%M:%S"))

# variables grlobales
# nom de l'index
index_name = "python_traffic"

# ré-çrée l'index ou maj
index_init = False

# nombre de ligne par requête
traffic_nb_rows = 100

# niveau de confiance des données
traffic_reliability = 5

# intervalle de requêtage et temps maximale
traffic_time_interval = 10
traffic_time_max = 30

# url
traffic_url = "https://data.rennesmetropole.fr/api/records/1.0/search/?dataset=etat-du-trafic-en-temps-reel&q=&rows="+str(traffic_nb_rows)

print(
    "\n\nInformations",
    "\n--> api traffic:",
    "\n----> url:", traffic_url,
    "\n----> nombre de lignes à prendre:", traffic_nb_rows,
    "\n----> reliability: >{}%".format(traffic_reliability),
    "\n----> rafraichissement: tous les {}s (max de {}s)".format(traffic_time_interval, traffic_time_max),
    "\n--> elasticsearch index:", index_name
)



# ### Connection elastic search
time.sleep(1)
print("\n\nConnection à elasticsearch")
# crée une connection elasticsearch
es = utils.connect_elasticsearch()



# ### Initialisation de l'index et mapping
time.sleep(1)
print(f"\n\nGestion de l'index '{index_name}'")

index_create = False
if not index_init:
    if es.indices.exists(index=index_name):
        index_init_text = "mise à jour"
    else:
        index_create = True
        index_init_text = "création"
else:
    index_create = True
    if es.indices.exists(index=index_name):
        index_init_text = "remplacement (après suppression)"
        es.indices.delete(index=index_name)
    else:
        index_init_text = "création"

print("--> opéation à réaliser sur l'index:", index_init_text)

# mappings pour les coordonnées geospatiales
req_body = {
    "mappings": {
        "properties": {
            "fields": {
                "properties": {
                    # fields.geo_point_2d
                    "geo_point_2d": { "type":"geo_point" },
                    
                    # fields.geo_shape
                    "geo_shape": { "type":"geo_shape" }
                }
            },
            
            "geometry": {
                "properties": {
                    # geometry.coordinates
                    "coordinates": { "type":"geo_point" }
                 }
             }
        }
    }
}

# crée l'índex vide
if index_create:
    es.indices.create(index=index_name, body=req_body)
    print("--> index bien créé!")
    
nb_rows_elastic1 = es.count(index=index_name)["count"]
print("--> nombre de documents dans l'index:", nb_rows_elastic1)



# ### Loop
time.sleep(1)
print("\n\nApi traffic to Elasticsearch")
traffic_nb_requete = int(traffic_time_max / traffic_time_interval)
print(f"--> il y a {traffic_nb_requete} requêtes à faire tous les {traffic_time_interval}s")

cpt = 1
while cpt<=traffic_nb_requete:
    print(f"\n--- Requête {cpt}/{traffic_nb_requete} ---")
    print("start:", time.strftime("%Y/%m/%d %H:%M:%S"))

    ### Import depuis l'api traffic
    print("\n- API traffic")
    
    # get
    traffic = requests.get(traffic_url)
    if traffic.status_code==200:
        print("--> requête ok!")
    else:
        print("--> requête non-ok!")
        print("----> erreur :", traffic.status_code)

    # les données
    data_json = traffic.json()
    data = data_json["records"]
    nb_rows1 = len(data)
    print(f"--> nombre de documents importés: {nb_rows1}/{traffic_nb_rows}")
    

    ### Data processing
    print("\n- Qualité des données")

    print("--> reliability...")
    data = [i for i in data if i["fields"]["traveltimereliability"]>=traffic_reliability]

    nb_rows2 = len(data)
    nb_rows3 = nb_rows1-nb_rows2
    print(f"----> nombre de documents restants: {nb_rows2}/{nb_rows1} ({nb_rows3} supprimés)")
    
    
    ### Export vers elasticsearch
    print("\n- Export vers elasticsearch")

    # export vers elastic
    print("...")
    i = es.count(index=index_name)['count']+1
    j = 0
    for doc_body in data:
        req = es.index(index=index_name, id=i, doc_type='_doc', body=doc_body)
        i = i+1
        j = j+1
    print(f"----> nombre de documents exportés: {j}/{nb_rows2}")
    
    
    ### attente / rafraichissement
    if cpt<traffic_nb_requete:
        print("\n(--attente--)")
        time.sleep(traffic_time_interval)
    cpt = cpt+1
    
print("\n- end:", time.strftime("%Y/%m/%d %H:%M:%S"))



# check elasticsearch
time.sleep(3)
nb_rows_elastic2 = es.count(index=index_name)["count"]
print(f"\n--> nombre total de documents dans l'index: {nb_rows_elastic2}/{nb_rows_elastic1}")

print("\nFin:", time.strftime("%Y/%m/%d %H:%M:%S"))
