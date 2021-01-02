import c4d
from c4d import gui
from datetime import datetime
from pprint import pprint

"""je n'obtiens pas exactement le m^ême nombre mais cela à l'air de focntionner pour renseigner le
   le champ time en dessous de 1970 -> nombre négatif"""
   
def esriTime(annee,mois = 1, jour = 1):
    timestamp = datetime(annee, mois,jour).strftime('%s')
    return (int(timestamp)*1000)

# Main function
def main():
    #exemples tirés de la doc esri rest api
    #time=1199145600000 (1 Jan 2008 00:00:00 GMT)
    #time=1199145600000, 1230768000000 (1 Jan 2008 00:00:00 GMT to 1 Jan 2009 00:00:00 GMT

    timestamp = datetime(1900, 1, 1).strftime('%s')

    #dans esri rest api cela doit ^être ne millisecondes ->*1000
    print(int(timestamp)*1000)
    print(esriTime(1900))

    #exemple d'url :
    #https://ge.ch/sitgags2/rest/services/CARTES_HISTORIQUES/CARTE_NATIONALE_25K_1956_2009/ImageServer/exportImage?bbox=2501394.5889073%2C1113994.9272232%2C2505009.5889073%2C1118794.9272232&bboxSR=&size=2048%2C2048&imageSR=&time=-420771600000&format=jpgpng&pixelType=U8&noData=&noDataInterpretation=esriNoDataMatchAny&interpolation=+RSP_BilinearInterpolation&compression=&compressionQuality=&bandIds=&mosaicRule=&renderingRule=&f=image

# Execute main()
if __name__=='__main__':
    main()