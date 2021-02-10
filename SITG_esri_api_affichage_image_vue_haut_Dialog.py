import c4d
import requests
# Welcome to the world of Python

CONTAINER_ORIGIN =1026473
ORIGIN_DEFAULT = c4d.Vector(2499430, 0, 1118370)

ID_SITG_RASTER_VUE_HAUT_CMD = 1056566

ID_ENABLED = 1
ID_URL_EXTRACT_IMG = 2
ID_LAYERID = 3
ID_BBOX = 4 #bbox sous forme de string
ID_SIZE = 5 #taille de l'image a extraire sous forme de string larg,haut



ID_GRPE_MAIN      = 1000
ID_COMBO_SERVER   = 1100
ID_COMBO_LAYER    = 1200

INITW = 300
INITH = 15

TXT_NOT_SAVED = "Le document doit être sauvegardé pour l'affichage.\nVoulez-vous l'enregistrer ?"
TXT_NOT_ORIGIN = "Le document n'est pas géoréférencé, les coordonnées par défaut vont être appliquées.\nVoulez vous continuer?"
TXT_NOT_METER = "Les unités du document ne sont pas en mètres, si vous continuez les unités seront modifiées.\nVoulez-vous continuer ?"


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
            return [(layer['id'],layer['name']) for layer in layers]


class DlgRasterDisplay(c4d.gui.GeDialog):

    lst_servers = [('SITG orthophotos historiques','https://ge.ch/sitgags2/rest/services/RASTER/ORTHOPHOTOS_HISTORIQUES/MapServer'),
                   ('SITG orthophotos IRC historiques','https://ge.ch/sitgags2/rest/services/RASTER/ORTHOPHOTOS_IRC_HISTORIQUES/MapServer')]

    layers = []

    def CreateLayout(self):
        self.SetTitle("Affichage raster dans la vue de haut")
        self.GroupBegin(ID_GRPE_MAIN,c4d.BFH_SCALE|c4d.BFV_SCALEFIT,cols = 2, rows =1)
        self.AddComboBox(ID_COMBO_SERVER,c4d.BFH_SCALE|c4d.BFV_SCALE, initw = INITW, inith = INITH)
        for i,(nom,url) in enumerate(self.lst_servers):
            self.AddChild(ID_COMBO_SERVER,ID_COMBO_SERVER+i+1,nom)
        self.AddComboBox(ID_COMBO_LAYER,c4d.BFH_SCALE|c4d.BFV_SCALE, initw = INITW, inith = INITH)
        self.GroupEnd()
        return True

    def InitValues(self):
        doc = c4d.documents.GetActiveDocument()
        bc = doc[ID_SITG_RASTER_VUE_HAUT_CMD]
        if not bc:
            bc = c4d.BaseContainer()
            bc[ID_URL_EXTRACT_IMG] = self.lst_servers[0][1]
            bc[ID_LAYERID] = 0

        bc[ID_ENABLED] = True
        doc[ID_SITG_RASTER_VUE_HAUT_CMD] = bc

        dic_url = {url:i for i,(nom,url) in enumerate(self.lst_servers)}
        i = dic_url[bc[ID_URL_EXTRACT_IMG]]

        self.majLayers(bc[ID_URL_EXTRACT_IMG])

        self.SetLong(ID_COMBO_SERVER, ID_COMBO_SERVER+1+i)
        nom,url = self.lst_servers[i]

        self.majLayers(url)

        return True

    def Command(self, id, msg):
        #LISTE SERVER
        if id==ID_COMBO_SERVER:
            i = self.GetLong(ID_COMBO_SERVER)-ID_COMBO_SERVER-1
            nom,url = self.lst_servers[i]
            self.majLayers(url)
        
        #LISTE LAYERS
        if id==ID_COMBO_LAYER:
            i = self.GetLong(ID_COMBO_LAYER)-ID_COMBO_LAYER-1
            print(self.layers[i])

        return True

    def DestroyWindow(self):
        #désactiver le chargement des orthos
        bc = doc[ID_SITG_RASTER_VUE_HAUT_CMD]
        bc[ID_ENABLED] = False
        doc[ID_SITG_RASTER_VUE_HAUT_CMD] = bc

    def majLayers(self, url):
        self.FreeChildren(ID_COMBO_LAYER)
        api = ESRI_api_rest_MapServer(url)
        self.layers = api.getLayers()
        for id_lyr,name in self.layers:
            self.AddChild(ID_COMBO_LAYER,ID_COMBO_LAYER+id_lyr+1,name)
        self.SetLong(ID_COMBO_LAYER, ID_COMBO_LAYER+1+self.layers[0][0])

def verifications(doc):
    #TODO : vérifier si on a pas une image déjà présente qui ne vient pas du plugin
    #verification du document qui doit être en metre
    usdata = doc[c4d.DOCUMENT_DOCUNIT]
    scale, unit = usdata.GetUnitScale()
    if  unit!= c4d.DOCUMENT_UNIT_M:
        rep = c4d.gui.QuestionDialog(TXT_NOT_METER)
        if not rep : return False
        unit = c4d.DOCUMENT_UNIT_M
        usdata.SetUnitScale(scale, unit)
        doc[c4d.DOCUMENT_DOCUNIT] = usdata
    #verification sauvegarde du document pour copier l'image dans le dossier tex
    path_doc = doc.GetDocumentPath()
    if path_doc == '':
        relatif = False
        rep = c4d.gui.QuestionDialog(TXT_NOT_SAVED)
        if not rep : return False

        c4d.CallCommand(12098) # Enregistrer le projet
        if not(doc.GetDocumentPath()) : return False
        
    #vérification géoréférencement du doc
    if not doc[CONTAINER_ORIGIN]:
        rep = c4d.gui.QuestionDialog(TXT_NOT_ORIGIN)
        if not rep : return False

        doc[CONTAINER_ORIGIN] = ORIGIN_DEFAULT

    return True

# Main function
def main():
    gui.MessageDialog('Hello World!')

# Execute main()
if __name__=='__main__':
    doc = c4d.documents.GetActiveDocument()
    if verifications(doc):
        dlg = DlgRasterDisplay()
        dlg.Open(c4d.DLG_TYPE_ASYNC)