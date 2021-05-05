# Projet traffic_rennes

Groupe : Fred, Khaly, Zaina


## Sujet

Afficher le traffic de la métropôle rennaise.

A faire :
* récupérer les données depuis l'api,
* les transférer vers elasticsearch,
* créer le dashboard sur kibana.

API données : https://data.rennesmetropole.fr/explore/dataset/etat-du-trafic-en-temps-reel/information/



</br>

## Utilisation

Utilisation de la v3.2 pour le transfert des données depuis l'api vers elasticsearch :

* définir les paramètres depuis ***trafficrennes_transfertdata_parameters.txt***
    * nom de l'index *(string)* : `index_name = traffic_rennes` 
    * re-créer l'index (`True`) ou le màj (`False`) *(bool)* : `index_init = False`
    * nombre de ligne à importer par requête *(int)* : `traffic_nb_rows = 1000`
    * niveau de confiance des données en % *(int)* : `traffic_reliability = 50`
    * temps d'attente entre chaque flux en s *(int/eval)* : `traffic_time_interval = 60*5` (60s=>1min\*5=>5min)
    * temps total que le programme tourme en s *(int/eval)* : `traffic_time_max = 60*60*3` (60s=>1min\*60=>1h*3=>3h)

* lancer le programme via ***.trafficrennes_transfertdata_run.bat***

* lancer le serveur kibana
    * créer un index-pattern<sup>1</sup> dont l'id est `trafficrennes-indexpatternid-x9y7z6`
    * importer le fichier ***trafficrennes_dashboard.ndjson***
    * le dashboard est disponible sous le nom `trafficrennes-dashboard`

*<sup>1</sup> la création d'un index-pattern nécéssite que l'index existe et soit non-vide.*



</br>

## Versionning

### v5 : dashboard kibana
Réalisation du dashboard sur kibana (v5.0).


### v4 : transfère elasticsearch via python
api -> python -> elasticsearch : via flask et docker, <br/>
A partir de la v3.0 et utilisation de flask<sup>2</sup> :
* v4.0 : création d'un formulaire web pour la définition des paramètres
* v4.1 : création d'une page web pour l'affichage de la log
* ~~v4.2 : dockerisation du programme python~~

Obsolète : impossible de réaliser l'affichage de la log en continue.

*<sup>2</sup> flask : framework python*


### v3 : transfère elasticsearch via python
api -> python -> elasticsearch : via batch-windows, <br/>
A partir de la v2.0 :
* v3.0 : création d'un flux continue pour la partie *appel api -> ... -> màj index elasticsearch*
* v3.1 : paramètres de personnalisation du process définis via un fichier externe
* v3.2 : lancement du programme python en **batch-windows**  

Réalisation de tests unitaires sur :
* fichiers externes
* type des paramètres 
* serveur elasticsearch
* api traffic


### v2 : transfère elasticsearch via python
api -> python -> elasticsearch : manuellement,  
Programme python qui appel l'api, récupère les données, les nettoies, et crée/màj l'index elasticsearch (v2.0).


### v1 : transfère elasticsearch via logstash
api -> logstash -> elasticsearch,  
Obsolète : elasticsearch ne reconnait pas automatiquement les champs géospatiales (v1.0).
