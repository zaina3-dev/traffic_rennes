# coding: utf-8

import json
from elasticsearch import Elasticsearch


def second_to_time(s, strftime_out=["j","h","m","s"]):
    """
    Convertir des secondes en jours, heures, minutes et secondes
    
    Parameters
    ----------
    s : int
        nombre de secondes en entrée

    strftime_out : list of string
        le format en sortie
    
    Returns
    -------
    String with the converted seconds.
    
    Notes
    -----
    j: jours, h:heures, m:minutes, s:secondes
    """

    # correspondance entre secondes et j,h,m,s
    x = {"j":(1*60*60)*24, "h":(1*60)*60, "m":(1)*60, "s":1}
    
    # filtre si strftime_out
    strftime_out = [i for i in strftime_out if i in x.keys()]
    x = {i:x[i] for i in strftime_out}
    
    y = {}
    for i in x.keys():
        y[i] = int(s/x[i])
        s = s%x[i]

    z = [str(y[i])+i for i in y.keys() if y[i]>0]
    z = " ".join(z)
    return z

# test le port elasticsearch
def connect_elasticsearch(host, port):
    es = None
    es = Elasticsearch([{'host':host, 'port':port}])
    if es.ping():
        print('--> elasticsearch bien connecté')
        es._connected = True
    else:
        server = host +':'+ str(port) +'/'
        print('--> /!\\ elasticsearch pas de réponse :', server)
        es._connected = False
    return es


# print le contenu d'un json
def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

