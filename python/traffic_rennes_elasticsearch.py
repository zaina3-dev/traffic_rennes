# coding: utf-8

'''
Programme qui va consommer l'api traffic rennes pour ensuite transférer ses données à elasticsearch : 
- windows (pré-requis)
--> programme lamcé en batch windows
--> ses paramètres sont à définir dans un fichier text sous la fome "nom = valeur"
--> le fichier des paramètres doit être passé en paramètre lors de l'appel du programme python en .bat
--> le script utils.py avec les fonctions python doit se trouver à la racine du programme

- python
--> on récupère le contenu du fichier des paramètres et on initialise les variables
----> si fichier non existant on utilise des valeurs par défauts
--> connection elasticsearch et gestion de l'index
--> stream-processing / loop
----> requête l ápi et récupère les données
----> nettoyage / validation
----> envoies à elasticsearch

- fin
'''


#%% librairies
import time
import sys
import requests
import utils



#%% ### Initialisation
time.sleep(1)
print("\nDébut-programme-python:", time.strftime("%Y/%m/%d %H:%M:%S"))

print("\n\nInformations")

# gestion des variables globales
# parametre fournit en cmd
cArgs = sys.argv 
#cArgs[0] pour script

print("- Fichier avec les paramètres")
params_file_exist = False
try:
    params_file = cArgs[1]
    params_file_exist = True
    print("-->", params_file)
except:
    print("--> /!\ non fourni")


if params_file_exist:
    params_sep = " = "

    # fichier avec les parametres sous la forme nom = valeur
    fichier = open(file=params_file, mode="r", newline="")
    params_list = [line.rstrip() for line in fichier.readlines() if (line[0]!='#' and params_sep in line)]
    fichier.close()
    
    params = {}
    for i in params_list:
        a = i.split(params_sep)
        params[a[0]] = a[1]
    
    # initialisation des parametres
    index_name = str(params["index_name"])
    index_init = params["index_init"]=='True'
    traffic_nb_rows = int(params["traffic_nb_rows"])
    traffic_reliability = int(params["traffic_reliability"])
    traffic_time_interval = int(params["traffic_time_interval"])
    traffic_time_max = int(params["traffic_time_max"])
    
else:
    # valeurs par defaut pour test
    print("--> les valeurs par défaut vont être utilisées")
    # nom de l'index
    index_name = "traffic_rennes"
    
    # ré-çrée l'index ou maj
    index_init = False
    
    # nombre de ligne par requête
    traffic_nb_rows = 10
    
    # niveau de confiance des données
    traffic_reliability = 5
    
    # intervalle de requêtage et temps maximale
    traffic_time_interval = 5
    traffic_time_max = 15

# url
traffic_url = "https://data.rennesmetropole.fr/api/records/1.0/search/?dataset=etat-du-trafic-en-temps-reel&q=&rows="+str(traffic_nb_rows)

print(
    "\n- Api traffic:",
    "\n--> url:", traffic_url,
    "\n--> nombre de lignes à prendre:", traffic_nb_rows,
    "\n--> reliability: >{}%".format(traffic_reliability),
    "\n--> rafraichissement: tous les {}s (max de {}s)".format(traffic_time_interval, traffic_time_max),
    
    "\n\n- Elasticsearch index:", index_name
)



#%% ### Connection elastic search
time.sleep(1)
print("\n\nConnection à elasticsearch")
# crée une connection elasticsearch
es = utils.connect_elasticsearch()



# ### Initialisation de l'index et mapping
time.sleep(1)
print(f"\n\nGestion de l'index '{index_name}'")

index_create = False
if index_init:
    index_create = True
    if es.indices.exists(index=index_name):
        index_init_text = "remplacement (après suppression)"
        es.indices.delete(index=index_name)
    else:
        index_init_text = "création"
else:
    if es.indices.exists(index=index_name):
        index_init_text = "mise à jour"
    else:
        index_create = True
        index_init_text = "création (car index non existant pour maj)"

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



#%% ### Loop
time.sleep(1)
print("\n\nApi traffic to Elasticsearch: stream-processing")
traffic_nb_requete = int(traffic_time_max / traffic_time_interval)
print(f"- stream-config: il y aura {traffic_nb_requete} requêtes à faire tous les {traffic_time_interval}s")

print("- stream-starts:", time.strftime("%Y/%m/%d %H:%M:%S"))
cpt = 1
while cpt<=traffic_nb_requete:
    print(f"\n--- Requête {cpt}/{traffic_nb_requete} ---")
    print("- lancement:", time.strftime("%Y/%m/%d %H:%M:%S"))

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
    print("--> export en cours...")
    i = es.count(index=index_name)['count']+1
    j = 0
    for doc_body in data:
        req = es.index(index=index_name, id=i, doc_type='_doc', body=doc_body)
        i = i+1
        j = j+1
    print(f"----> nombre de documents exportés: {j}/{nb_rows2}")
    
    
    ### attente / rafraichissement
    if cpt<traffic_nb_requete:
        print(f"\n(--- attente-de-{traffic_time_interval}s-avant-nouvel-appel-api ---)\n")
        time.sleep(traffic_time_interval)
    cpt = cpt+1
    
print("\n- stream-ends:", time.strftime("%Y/%m/%d %H:%M:%S"))



#%% check elasticsearch
time.sleep(3)
print("\n\nElasticsearch")
nb_rows_elastic2 = es.count(index=index_name)["count"]
print(f"--> nombre total de documents dans l'index: {nb_rows_elastic2}/{nb_rows_elastic1}")

print("\nFin-programme-python:", time.strftime("%Y/%m/%d %H:%M:%S"))
