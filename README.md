# Projet traffic_rennes

Groupe : Fred, Khaly, Zaina


## Sujet

Afficher le traffic de la métropôle rennaise.

A faire :
* récupérer les données depuis l'api,
* les transférer vers elasticsearch,
* créer un dashboard kibana.

API données : https://data.rennesmetropole.fr/explore/dataset/etat-du-trafic-en-temps-reel/information/



## Versionning

### v4 : dashboard kibana
Réalisation du dashboard sur kibana.


### v4 : transfère elasticsearch via python
**api -> python -> elasticsearch : via flask et docker**, <br/>
A partir de la v3.0 et utilisation de flask :
* v4.0 : création d'un formulaire web pour la définition des paramètres
* v4.1 : création d'une page web pour l'affichage de la log
* v4.2 : dockerisation du programme python (non-fait)

Obsolète : impossible de réaliser l'affichage de la log en continue.


### v3 : transfère elasticsearch via python
**api -> python -> elasticsearch : via batch-windows**, <br/>
A partir de la v2.0 :
* v3.0 : création d'un flux continue pour la partie appel api ->...-> màj index elasticsearch
* v3.1 : paramètres de personnalisation du process définis via un fichier externe
* v3.2 : lancement du programme python via **batch-windows**


### v2 : transfère elasticsearch via python
**api -> python -> elasticsearch : manuellement**, <br/>
Programme python qui appel l'api, récupère les données, les nettoies, et crée/màj l'index elasticsearch (v2.0).


### v1 : transfère elasticsearch via logstash
**api -> logstash -> elasticsearch**, <br/>
Obsolète : elasticsearch ne reconnait pas automatiquement les champs géospatiales.
