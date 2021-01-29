import c4d
import requests
from pprint import pprint
from datetime import datetime

"""Pour ces catalogues on peurt soit récupérer les ObjectID soit utiliser le time
   les descriptions des ObjectId contiennent la date de début et de fin ce qui évite de charger
   des images en trop. Je pense donc que le mieux est d'utiliser time, mais en sachant quelles années
   prendre avec la description.

   Pour les plan d'ensemble c'est un peu plus complexe, à creuser selon les deux catalogues à dispo"""

#-> #exemple d'url utilisant time dans un catalogue:
#https://ge.ch/sitgags2/rest/services/CARTES_HISTORIQUES/CARTE_NATIONALE_25K_1956_2009/ImageServer/exportImage?bbox=2501394.5889073%2C1113994.9272232%2C2505009.5889073%2C1118794.9272232&bboxSR=&size=2048%2C2048&imageSR=&time=-420771600000&format=jpgpng&pixelType=U8&noData=&noDataInterpretation=esriNoDataMatchAny&interpolation=+RSP_BilinearInterpolation&compression=&compressionQuality=&bandIds=&mosaicRule=&renderingRule=&f=image


# exemple url utilisant le n° de l'OBECTID dans mosaicRule (where) -> &mosaicRule={"where":"OBJECTID=6"}
#https://ge.ch/sitgags2/rest/services/CARTES_HISTORIQUES/CARTES_DUFOUR_1845_1935/ImageServer/exportImage?bbox=2497710.4221322434%2C1115356.7250581598%2C2502269.79435767%2C1119925.2434665866&bboxSR=&size=&imageSR=&time=&format=jpgpng&pixelType=U8&noData=&noDataInterpretation=esriNoDataMatchAny&interpolation=+RSP_BilinearInterpolation&compression=&compressionQuality=&bandIds=&mosaicRule={"where":"OBJECTID=6"}&renderingRule=&f=image

def esriTime(annee,mois = 1, jour = 1):
    date = datetime(annee,mois,jour)
    return int(datetime.timestamp(date)*1000)


# Main function
def main():
    #lecture du dossier source
    #url_base = 'https://ge.ch/sitgags2/rest/services/RASTER/Orthophotos_1932_2012/ImageServer'
    #url_base = 'https://ge.ch/sitgags2/rest/services/RASTER/ORTHOPHOTOS/ImageServer'

    #attention plan d'ensemble complet comprenant 366 images !!'
    #url_base = 'https://ge.ch/sitgags2/rest/services/CARTES_HISTORIQUES/PLAN_BASE_ARCHIVE_1936_2002/ImageServer'

    #plan d'ensemble simplifié à étudier !'
    #url_base = 'https://ge.ch/sitgags2/rest/services/CARTES_HISTORIQUES/PLAN_BASE_test/ImageServer'

    url_base = 'https://ge.ch/sitgags2/rest/services/CARTES_HISTORIQUES/CARTES_DUFOUR_1845_1935/ImageServer'
    #url_base = 'https://ge.ch/sitgags2/rest/services/CARTES_HISTORIQUES/CARTES_SIEGFRIED_1891_1945/ImageServer'
    #url_base =  'https://ge.ch/sitgags2/rest/services/CARTES_HISTORIQUES/CARTE_NATIONALE_25K_1956_2009/ImageServer'

    url_query =url_base+'/query?'
    #url_query =url_base+'/exportImage?'
    time = esriTime(1907,mois = 2, jour = 1)
    print(time)

    params = { "f" :"json",
                "bbox" : "2497091.044035166,1114613.600600382,2502875.8100028946,1120546.846187405",
                "time" : f"{time}",
                "size" : "1024,1024",
    }

    params = { "f" :"json",

    }


    r = requests.get(url_query,params = params)
    #pprint(dir(r))
    print(r.url)


    if r.status_code == 200:
        #pprint(r.json())

        for feature in  r.json()['features']:
            objID = feature['attributes']['OBJECTID']
            url = f"{url_base}/{objID}"
            r2 = requests.get(url,params = params)
            #infos pour chaque layer emprise et dates début et fin
            pprint(r2.json())
            attr = r2.json()['attributes']
            #pprint(attr)
            #pts = [c4d.Vector(x,0,z) for x,z in r2.json()['geometry']['rings'][0]]
            #print(pts)
            #pour l'extraction de chaque layer:
            #https://ge.ch/sitgags2/rest/services/CARTES_HISTORIQUES/CARTE_NATIONALE_25K_1956_2009/ImageServer/4/image?bbox=2480000,1110000,2515000,1134000'
            print('-------------')


# Execute main()
if __name__=='__main__':
    main()