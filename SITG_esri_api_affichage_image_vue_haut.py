
import c4d
import requests
from pprint import pprint
import os
from datetime import datetime


CONTAINER_ORIGIN =1026473

NOT_SAVED_TXT = "Le document doit être enregistré pour pouvoir copier les textures dans le dossier tex, vous pourrez le faire à la prochaine étape\nVoulez-vous continuer ?"
DOC_NOT_IN_METERS_TXT = "Les unités du document ne sont pas en mètres, si vous continuez les unités seront modifiées.\nVoulez-vous continuer ?"


O_DEFAUT = c4d.Vector(2500000.00,0.0,1120000.00)

URL = 'https://ge.ch/sitgags2/rest/services/RASTER/ORTHOPHOTOS_HISTORIQUES/MapServer/export?'
FORMAT = 'png'

NOM_DOSSIER_IMG = 'tex/__back_image'

def empriseVueHaut(bd,origine):

    dimension = bd.GetFrame()
    largeur = dimension["cr"]-dimension["cl"]
    hauteur = dimension["cb"]-dimension["ct"]

    mini =  bd.SW(c4d.Vector(0,hauteur,0)) + origine
    maxi = bd.SW(c4d.Vector(largeur,0,0)) + origine

    return  mini,maxi,largeur,hauteur

def main():

    #le doc doit être en mètres
    doc = c4d.documents.GetActiveDocument()

    usdata = doc[c4d.DOCUMENT_DOCUNIT]
    scale, unit = usdata.GetUnitScale()
    if  unit!= c4d.DOCUMENT_UNIT_M:
        rep = c4d.gui.QuestionDialog(DOC_NOT_IN_METERS_TXT)
        if not rep : return
        unit = c4d.DOCUMENT_UNIT_M
        usdata.SetUnitScale(scale, unit)
        doc[c4d.DOCUMENT_DOCUNIT] = usdata

    #si le document n'est pas enregistré on enregistre
    path_doc = doc.GetDocumentPath()

    while not path_doc:
        rep = c4d.gui.QuestionDialog(NOT_SAVED_TXT)
        if not rep : return
        c4d.documents.SaveDocument(doc, "", c4d.SAVEDOCUMENTFLAGS_DIALOGSALLOWED, c4d.FORMAT_C4DEXPORT)
        c4d.CallCommand(12098) # Enregistrer le projet
        path_doc = doc.GetDocumentPath()

    dossier_img = os.path.join(path_doc,NOM_DOSSIER_IMG)

    origine = doc[CONTAINER_ORIGIN]
    if not origine:
        doc[CONTAINER_ORIGIN] = O_DEFAUT
        origine = doc[CONTAINER_ORIGIN]
    bd = doc.GetActiveBaseDraw()
    camera = bd.GetSceneCamera(doc)
    if not camera[c4d.CAMERA_PROJECTION]== c4d.Ptop:
        c4d.gui.MessageDialog("""Ne fonctionne qu'avec une caméra en projection "haut" """)
        return

    #pour le format de la date regarder : https://docs.python.org/fr/3/library/datetime.html#strftime-strptime-behavior
    dt = datetime.now()
    suffixe_time = dt.strftime("%y%m%d_%H%M%S")

    fn = f'ortho{suffixe_time}.{FORMAT}'
    #ID du layer 0= dernière orthophoto normalement
    id_lyr = 0



    mini,maxi,larg,haut = empriseVueHaut(bd,origine)
    #print mini.x,mini.z,maxi.x,maxi.z
    bbox = '{0}%2C{1}%2C{2}%2C{3}'.format(mini.x,mini.z,maxi.x,maxi.z) # 2499639.5233%2C1117120.08436258%2C2500839.57718198%2C1118560.1287&
    size = '{0},{1}'.format(larg,haut)
    #bboxSR = '2056'
    #imageSR = '2056'
    #url = 'http://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/export?bbox={0}&format=jpg&size={1}&f=image&bboxSR={2}&imageSR={3}'.format(bbox,size,bboxSR,imageSR)
    params ={"f":"json",
             "bbox":f"{mini.x},{mini.z},{maxi.x},{maxi.z}",
             "size":f"{larg},{haut}",
             "format": FORMAT,
             "layers":f"show:{id_lyr}"}
    r = requests.get(URL,params)
    #print(r.url)
    #print(f"{mini.x},{mini.z},{maxi.x},{maxi.z}")
    #print(f"{larg},{haut}")

    if r.status_code ==200:
        if not os.path.isdir(dossier_img):
            os.makedirs(dossier_img)
        rjson = r.json()
        extent = rjson['extent']
        url_img = rjson['href']
        ext = url_img[-4:]
        r_img = requests.get(url_img)

        if r_img.status_code == 200:
            with open(os.path.join(dossier_img,fn), 'wb') as f:
                for chunk in r_img.iter_content(1024):
                    f.write(chunk)

    #on récupère l'ancienne image
    old_fn = os.path.join(dossier_img,bd[c4d.BASEDRAW_DATA_PICTURE])

    bd[c4d.BASEDRAW_DATA_PICTURE] = fn
    bd[c4d.BASEDRAW_DATA_SIZEX] = maxi.x-mini.x
    bd[c4d.BASEDRAW_DATA_SIZEY] = maxi.z-mini.z


    bd[c4d.BASEDRAW_DATA_OFFSETX] = (maxi.x+mini.x)/2 -origine.x
    bd[c4d.BASEDRAW_DATA_OFFSETY] = (maxi.z+mini.z)/2-origine.z
    #bd[c4d.BASEDRAW_DATA_SHOWPICTURE] = False

    #suppression de l'ancienne image
    #TODO : s'assurer que c'est bien une image générée NE PAS SUPPRIMER N'IMPORTE QUOI !!!
    if os.path.exists(old_fn):
        try : os.remove(old_fn)
        except : pass

    #bd.Message(c4d.MSG_UPDATE)
#
    #c4d.DrawViews(c4d.EVENT_ENQUEUE_REDRAW)

    c4d.EventAdd(c4d.EVENT_FORCEREDRAW)
    #c4d.GeSyncMessage(c4d.EVMSG_UPDATEBASEDRAW)


if __name__=='__main__':
    main()