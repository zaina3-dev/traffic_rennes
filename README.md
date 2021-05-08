# Projet traffic_rennes

Groupe : Fred, Khaly, Zaina


## Sujet

Afficher le traffic en temps réel de la métropôle rennaise.

A faire :
* récupérer les données depuis l'api,
* les transférer vers elasticsearch,
* créer le dashboard sur kibana.

API rennesmetropole : https://data.rennesmetropole.fr/explore/dataset/etat-du-trafic-en-temps-reel/information/



</br>

## Utilisation

### Prérequis
* serveur elasticsearch et kibana actifs
* api traffic rennes disponible
* python3 installé
* le contenu du répertoire "[binaires](../../tree/master/binaires/)"
    * programme batch qui lance le programme python (.bat)
    * programme python qui réalise le transfert de données (.py)
    * script python utils pour les fonctions (.py)
    * fichier des paramètres de configuration (.txt)
    * script docker-compose pour la création d'une stack (.yml)
    * données de création du dashboard (.ndjson)

Note :
* "[documents](../../tree/master/documents/)" contient la documentation fonctionnelle et technique
* "[releases](../../tree/master/releases/)" contient les scripts pour les anciennes versions


### Transfert des données depuis l'api vers elasticsearch
* définir les paramètres depuis le fichier des paramètres ***trafficrennes_transfertdata_parameters.txt***<sup>1</sup>
    * nom de l'index *(string)* : `index_name = traffic_rennes` 
    * re/créer l'index (`True`) ou le màj (`False`) *(bool)* : `index_init = False`
    * nombre de ligne à importer par requête *(int)* : `traffic_nb_rows = 1000`
    * indice de confiance des données en % *(int)* : `traffic_reliability = 10`
    * durée d'actualisation (attente entre chaque flux) en s *(int/eval)* : `traffic_time_interval = 60*5` (60s=>1min\*5=>5min)
    * durée total du flux-continu en s *(int/eval)* : `traffic_time_max = 60*60*1` (60s=>1min\*60=>60min=>1h)

* lancer le programme batch via ***.trafficrennes_transfertdata_run.bat***
    * le batch va exécuter le programme python (***trafficrennes_transfertdata.py***) avec le fichier des paramètres comme argument<sup>2</sup>
    * le script python utils (***trafficrennes_transfertdata_utils.py***) doit se trouver dans le même répertoire que le programme python

*<sup>1</sup> note : sont définis ici les valeurs par défaut du programme.*  

*<sup>2</sup> `python "trafficrennes_transfertdata.py" "trafficrennes_transfertdata_parameters.txt"`*


### Import du dashboard sous kibana
* créer un index-pattern<sup>3</sup> dont l'id est `trafficrennes-indexpatternid-x9y7z6`
* importer un saved-object avec le fichier ***trafficrennes_dashboard.ndjson***
* le dashboard est disponible sous le nom `trafficrennes-dashboard`

*<sup>3</sup> note : la création d'un index-pattern nécéssite que l'index existe et soit non-vide.*



</br>

## Versionning

### v5 : dashboard kibana
Réalisation du dashboard sur kibana (v5.0).


### v4 : transfert api to elasticsearch via python/flask
api -> python -> elasticsearch : via flask et docker, <br/>
A partir de la v3.0 et utilisation de flask<sup>4</sup> :
* v4.0 : création d'un formulaire web pour la définition des paramètres
* v4.1 : création d'une page web pour l'affichage de la log
* ~~v4.2 : dockerisation du programme python~~

Obsolète : impossible de réaliser l'affichage de la log en continue sur le navigateur.

*<sup>4</sup> flask : framework python*


### v3 : transfert api to elasticsearch via python
api -> python -> elasticsearch : via batch-windows, <br/>
A partir de la v2.0 :
* v3.0 : création d'un flux-continu pour la partie *appel api -> transformation des données -> màj index elasticsearch*
* v3.1 : paramètres de configuration du programme définis via un fichier texte externe
* v3.2 : lancement du programme python en **batch-windows**  

Réalisation de tests unitaires sur :
* l'existence des fichiers externes
* le type des paramètres 
* l'accessibilité au serveur elasticsearch (ping)
* la disponibilité de l'api traffic (réponse 200)


### v2 : transfert api to elasticsearch via python
api -> python -> elasticsearch : manuellement,  
v2.0 : programme python qui appel l'api, récupère les données, les nettoies, et crée/màj l'index elasticsearch.


### v1 : transfère elasticsearch via logstash
api -> logstash -> elasticsearch,  
v1.0 : obsolète, elasticsearch ne reconnait pas automatiquement les champs géospatiales.


### v0 : serveur elastic
ELK sera installé sur une image docker, avec :
* portainer : [localhost:9000/](http://localhost:9000/)
* elasticsearch : [localhost:9200/](http://localhost:9200/)
* kibana : [localhost:5601/](http://localhost:5601/)

v0.1 : le paramètrage des containers elasticsearch et kibana est défini dans un docker-compose.
