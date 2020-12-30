# coding: utf8


import json,sys,os

from urllib.request import urlopen

""" envoyer un subprocess du type:
    subprocess.Popen(['python','/Users/donzeo/Library/Preferences/MAXON/CINEMA 4D R17_89538A46/library/scripts/SITG/subprocess/requete_REST_ESRI_vecteur.py',url,fn_res])
    url = requete url REST avec un resultat f=pjson
    fn_res = nom complet du fichier de destination d el'image

    le resultat est l'ecriture du fichier image avec un ficchier json portant le meem nom pour le calage"""

def main():
    url = 'https://hepiageo2.hesge.ch/server/rest/services/geneve/bati3D/FeatureServer/6/query?geometry=2499243.77856,1118385.2987,2499576.80149,1118605.39344&f=json'
    fn_json = '/Users/olivier.donze/TEMP/test_rest_sitg/test_extraction_toit3D.json'

    
    #lecture de la requete json via rest
    site = urlopen(url)
    txt = site.read()
    dic_json = json.loads(txt)
    site.close()

    #ecriture du fichier json 
    with open(fn_json,'w') as f:
        f.write(json.dumps(dic_json,indent =4))


if __name__=='__main__':
    main()