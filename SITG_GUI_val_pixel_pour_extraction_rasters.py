import c4d
import math, requests, json

# Script state in the menu or the command palette
# Return True or c4d.CMD_ENABLED to enable, False or 0 to disable
# Alternatively return c4d.CMD_ENABLED|c4d.CMD_VALUE to enable and check/mark
#def state():
#    return True

TXT_TITLE_DLG = "Extraction de raster"

NB_PX_MAX = 4096 #pixels maximum pour l'extraction'
TAILLE_MIN_PX = 0.5
TAILLE_MAX_PX = 50

ID_VAL_PX = 1050
ID_INFO_SIZE = 1051
ID_INFO_RES = 1052
ID_COMBO_SRCE = 1053
ID_BTON_EXTRACT = 1054

MARGE_TOP = 1

def imageFromESRIrest(url,minx,minz,maxx,maxz,px_larg,px_haut,format = 'jpg', id_layer = -1, where = None, time = None):
    """return a json file from MapServer without layer
       where example = 'OBJECTID=d1' """
    if 'MapServer' in url:
        url += '/export?'
    elif 'ImageServer' in url:
        url += '/exportImage?'

    params = { 'f':'json',
               "bbox":f"{minx},{minz},{maxx},{maxz}",
               "size":f"{px_larg},{px_haut}",
               "format": format,
               "transparent":"true",
    }

    if id_layer > -1:
        params["layers"] = f"show:{id_layer}"

    if where:
        params['mosaicRule']= f'{{"where":"{where}"}}'

    if time:
        params['time'] = time

    r = requests.get(url,params)
    if r.status_code == 200:
        return r.json()
    else :
        return None

class DlgExtractRaster(c4d.gui.GeDialog):
    servers = [ 'MNT SITG',
                'MNS SITG',
                'MNT ESRI']

    def __init__(self, xmin,ymin,xmax,ymax):
        self.xmin,self.ymin,self.xmax,self.ymax = xmin,ymin,xmax,ymax
        self.larg = self.xmax-self.xmin
        self.haut = self.ymax-self.ymin
        self.surface = self.larg * self.haut


    def CreateLayout(self):
        self.SetTitle(TXT_TITLE_DLG)

        self.GroupBegin(500, flags=c4d.BFH_FIT, cols=2, rows=1)
        self.GroupBorderSpace(30, 30, 30, 0)
        self.AddStaticText(501,name="Serveur : ", flags=c4d.BFH_MASK, initw=100)
        self.AddComboBox(ID_COMBO_SRCE,flags=c4d.BFH_SCALEFIT, initw=250)
        self.GroupEnd()



        #self.GroupBegin(800, flags=c4d.BFH_CENTER, cols=1, rows=1)
        #self.GroupBorderSpace(30, MARGE_TOP, 30, 0)
        #self.AddStaticText( ID_INFO_RES, flags=c4d.BFH_CENTER, initw=0, inith=0, name= f'largeur : {self.larg:,.1f} m ; hauteur : {self.larg:,.1f} m ; surface de {self.surface:,.1f} m2'.replace(",","'"))
        #self.GroupEnd()

        self.GroupBegin(700, flags=c4d.BFH_FIT, cols=2, rows=1)
        self.GroupBorderSpace(30, MARGE_TOP, 30, 0)
        self.AddStaticText( 701, flags=c4d.BFH_FIT, initw=0, inith=0, name= 'Valeur du pixel : ', borderstyle=0)
        self.AddEditSlider(ID_VAL_PX, flags=c4d.BFH_SCALEFIT, initw=0, inith=0)
        self.GroupEnd()

        self.GroupBegin(600, flags=c4d.BFH_FIT, cols=1, rows=1)
        self.GroupBorderSpace(30, MARGE_TOP, 30, 0)
        #surface = round(self.larg)*round(self.haut)
        #self.AddStaticText( 601, flags=c4d.BFH_SCALEFIT, initw=0, inith=0, name= f'{self.larg:,.0f} m x {self.haut:,.0f} m = {surface:,.0f} m2'.replace(",","'"))
        self.AddStaticText(ID_INFO_RES, flags=c4d.BFH_FIT, initw=0, inith=0, name= "100'000 x 100'000 = 100'000'000 pixels")
        self.GroupEnd()

        self.GroupBegin(900, flags=c4d.BFH_CENTER, cols=1, rows=1)
        self.GroupBorderSpace(30, MARGE_TOP, 30, 30)
        self.AddButton(ID_BTON_EXTRACT, flags=c4d.BFH_CENTER, inith=20, name="extraire")
        self.GroupEnd()



        return True

    def InitValues(self):
        #calcul du minimum par rapport au nombre de pixel max
        mini = max(self.larg,self.haut)/NB_PX_MAX
        mini = math.ceil(mini*10)/10
        if TAILLE_MIN_PX>mini:
            mini = TAILLE_MIN_PX

        self.SetFloat( ID_VAL_PX, mini*2, min=mini, max=TAILLE_MAX_PX, step=.5, format=c4d.FORMAT_METER, min2=mini, max2=TAILLE_MAX_PX*5)
        #self.SetMeter(ID_VAL_PX,  mini*2, min=mini, max=TAILLE_MAX_PX, step=.5)
        self.majResult()

        #combo
        for i,txt in enumerate(self.servers):
            self.AddChild(ID_COMBO_SRCE,i,txt)

        return True

    def majResult(self):
        val_px = self.GetFloat(ID_VAL_PX)
        self.nb_px_x = int(round(self.larg/ val_px))
        self.nb_px_y = int(round(self.haut/ val_px))
        nb_px = self.nb_px_x * self.nb_px_y
        txt = f"{self.nb_px_x:,} x {self.nb_px_y:,} = {nb_px:,} pixels".replace(",","'")
        self.SetString(ID_INFO_RES,txt)

    def Command(self, id, msg):

        if id == ID_VAL_PX:
            self.majResult()

        if id== ID_BTON_EXTRACT:
            url = 'https://ge.ch/sitgags2/rest/services/RASTER/MNA_TERRAIN/ImageServer'
            #attention tiff avec deux f
            rjson = imageFromESRIrest(url,self.xmin,self.ymin,self.xmax,self.ymax,self.nb_px_x,self.nb_px_y,format = 'tiff')
            
            url_img = rjson.get('href')

            if url_img:
                downloadImg(url)
            else:
                c4d.gui.MessageDialog("Un problème est survenu, téléchargement impossible")


        return True

def downloadImg(url):
    print(url)
    pass

def main(xmin,ymin,xmax,ymax):
    #xmin,ymin,xmax,ymax =2496899.471763778,1117463.453163715,2501059.0292007225,1121783.1318230564
    dlg = DlgExtractRaster( xmin,ymin,xmax,ymax)
    dlg.Open(c4d.DLG_TYPE_MODAL)



# Execute main()
if __name__=='__main__':
    xmin,ymin,xmax,ymax =2496899.471763778,1117463.453163715,2501059.0292007225,1121783.1318230564
    main(xmin,ymin,xmax,ymax)
    