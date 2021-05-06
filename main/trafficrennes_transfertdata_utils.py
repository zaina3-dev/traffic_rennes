# coding: utf-8

import json
from elasticsearch import Elasticsearch


def second_to_time(s, strftime_out=["j","h","m","s"]):
    """
    Convertir des secondes en jours, heures, minutes et secondes.
    
    Parameters
    ----------
    s : int
        nombre de secondes en entrée

    strftime_out : list of str
        le format en sortie
    
    Examples
    -------
    second_to_time(s=93790) => '1j 2h 3m 10s'
    second_to_time(s=93790, strftime_out=['h','m']) => '26h 3m'

    Returns
    -------
    Durée correspond au nombre de secondes (str).
    
    Notes
    -----
    j:jours, h:heures, m:minutes, s:secondes
    """
    # correspondance entre j,h,m,s et secondes
    # ex: 1j = (1h)*24 = ([1m]*60)*24 = ([1s*60]*60)*24 = 86400s
    x = {'j':(1*60*60)*24, 'h':(1*60)*60, 'm':(1)*60, 's':1}
    
    # filtre si strftime_out
    strftime_out = [i for i in strftime_out if i in x.keys()]
    x = {i:x[i] for i in strftime_out}
    
    # calcul de la correspondance entre secondes et j,h,m,s
    # ex: 100000s => .(/86400)=1j +13600s(/3600)=>3h +2800s(/60)=>46m +40s
    # --------->  => 1j 3h 46m 40s
    y = {}
    for i in x.keys():
        y[i] = int(s/x[i])
        s = s%x[i]

    # création du str en sortie
    z = [str(y[i])+i for i in y.keys() if y[i]>0]
    z = '-'.join(z)
    return z


def connect_elasticsearch(host, port):
    """
    Test le server elasticsearch.
    
    Parameters
    ----------
    host : str
    port : int

    Returns
    -------
    Objet 'Elasticsearch' avec la propriété '._connected' permettant de savoir si bien connecté à elasticsearch.
    """
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


def jprint(obj):
    """
    Print le contenu d'un json.
    
    Parameters
    ----------
    obj : json

    Returns
    -------
    None, et print du du contenu de objet.
    """
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)
