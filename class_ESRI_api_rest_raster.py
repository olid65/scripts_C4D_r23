import c4d
import requests
from pprint import pprint

CONTAINER_ORIGIN =1026473

O_DEFAUT = c4d.Vector(2500000.00,0.0,1120000.00)

ID_SITG_RASTER_VUE_HAUT_CMD = 1056566
ID_SITG_RASTER_VUE_HAUT_MSGDATA = 1056565


ID_ENABLED = 1
ID_URL_EXTRACT_IMG = 2
ID_LAYERID = 3
ID_BBOX = 4 #bbox sous forme de string
ID_SIZE = 5 #taille de l'image a extraire sous forme de string larg,haut

URL_DEFAULT = 'https://ge.ch/sitgags2/rest/services/RASTER/ORTHOPHOTOS_HISTORIQUES/MapServer'
LAYERID_DAFAULT = 0
BBOX_DEFAULT = '2498577.226970822,1117523.9690901646,2500345.956204395,1119078.0240631981'




# Script state in the menu or the command palette
# Return True or c4d.CMD_ENABLED to enable, False or 0 to disable
# Alternatively return c4d.CMD_ENABLED|c4d.CMD_VALUE to enable and check/mark
#def state():
#    return True

class ESRI_api_rest(object):
    def __init__(self, url_base):
        self.url_base = url_base

class ESRI_api_rest_MapServer(ESRI_api_rest):

    def getLayers(self):
        url = self.url_base+'/layers?'
        params = {'f':'json'}
        r = requests.get(url, params)
        if r.status_code == 200:
            layers = r.json().get('layers',None)
            if not layers : return None
            return {layer['id']:layer['name'] for layer in layers}


# Main function
def main():
    doc = c4d.documents.GetActiveDocument()
    bc = doc[ID_SITG_RASTER_VUE_HAUT_CMD]

    bc = c4d.BaseContainer()
    bc.SetBool(ID_ENABLED, True)
    bc.SetString(ID_URL_EXTRACT_IMG,URL_DEFAULT)
    bc.SetInt32(ID_LAYERID, LAYERID_DAFAULT)
    

    doc[ID_SITG_RASTER_VUE_HAUT_CMD] = bc




    mapServer = ESRI_api_rest_MapServer('https://ge.ch/sitgags2/rest/services/RASTER/ORTHOPHOTOS_HISTORIQUES/MapServer')
    pprint(mapServer.getLayers())

# Execute main()
if __name__=='__main__':
    main()