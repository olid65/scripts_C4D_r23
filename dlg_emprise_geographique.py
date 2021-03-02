# -*- coding: utf-8 -*-

import c4d
import shapefile
import os,sys
from datetime import datetime


sys.path.append(os.path.dirname(__file__))

import SITG_esri_api_affichage_image_vue_haut as vue_haut
import SITG_GUI_val_pixel_pour_extraction_rasters as mnt

import ESRI_REST_API_Rasters as api_raster
import ESRI_API_SERVERS as api_servers




# Script state in the menu or the command palette
# Return True or c4d.CMD_ENABLED to enable, False or 0 to disable
# Alternatively return c4d.CMD_ENABLED|c4d.CMD_VALUE to enable and check/mark
# def state():
#    return True

CONTAINER_ORIGIN = 1026473

ORIGIN_DEFAULT = c4d.Vector(2499430.,0, 1118370.)

TAILLE_CADRAGE_DEFAUT = 1000

NOM_DOSSIER_IMG = 'tex/__back_image'

NOT_SAVED_TXT = "Le document doit être enregistré pour pouvoir copier les textures dans le dossier tex, vous pourrez le faire à la prochaine étape\nVoulez-vous continuer ?"

def verifDocSaved(doc):
    path_doc = doc.GetDocumentPath()

    while not path_doc:
        rep = c4d.gui.QuestionDialog(NOT_SAVED_TXT)
        if not rep : return False
        c4d.documents.SaveDocument(doc, "", c4d.SAVEDOCUMENTFLAGS_DIALOGSALLOWED, c4d.FORMAT_C4DEXPORT)
        c4d.CallCommand(12098) # Enregistrer le projet
        path_doc = doc.GetDocumentPath()

    return True

def getFileName(path_doc, ext='.jpg', prefixe = 'ortho'):
    dossier_img = os.path.join(path_doc,NOM_DOSSIER_IMG)
    if not os.path.isdir(dossier_img):
            os.makedirs(dossier_img)

    #pour le format de la date regarder : https://docs.python.org/fr/3/library/datetime.html#strftime-strptime-behavior
    dt = datetime.now()
    suffixe_time = dt.strftime("%y%m%d_%H%M%S")

    fn = f'{prefixe}_{suffixe_time}{ext}'
    return os.path.join(dossier_img,fn)

def modifDisplay(bd,fn, mini,maxi,origine):
    dossier_img = os.path.dirname(fn)
    #on récupère l'ancienne image
    old_fn = os.path.join(dossier_img,bd[c4d.BASEDRAW_DATA_PICTURE])

    bd[c4d.BASEDRAW_DATA_PICTURE] = os.path.basename(fn)
    bd[c4d.BASEDRAW_DATA_SIZEX] = maxi.x-mini.x
    bd[c4d.BASEDRAW_DATA_SIZEY] = maxi.z-mini.z


    bd[c4d.BASEDRAW_DATA_OFFSETX] = (maxi.x+mini.x)/2 -origine.x
    bd[c4d.BASEDRAW_DATA_OFFSETY] = (maxi.z+mini.z)/2-origine.z
    #bd[c4d.BASEDRAW_DATA_SHOWPICTURE] = False

    #suppression de l'ancienne image
    if os.path.exists(old_fn):
        #par sécurité on regarde que le chemin a notre nom_dossier
        #pour éviter d'effacer un truc important TODO -> améliorer le controle ???
        if NOM_DOSSIER_IMG in old_fn:
            try : os.remove(old_fn)
            except : pass
    c4d.EventAdd(c4d.EVENT_FORCEREDRAW)


def empriseVueHaut(bd, origine):
    dimension = bd.GetFrame()
    largeur = dimension["cr"] - dimension["cl"]
    hauteur = dimension["cb"] - dimension["ct"]

    mini = bd.SW(c4d.Vector(0, hauteur, 0)) + origine
    maxi = bd.SW(c4d.Vector(largeur, 0, 0)) + origine

    return mini, maxi, largeur, hauteur


def empriseObject(obj, origine):
    mg = obj.GetMg()

    rad = obj.GetRad()
    centre = obj.GetMp()

    # 4 points de la bbox selon orientation de l'objet
    pts = [c4d.Vector(centre.x + rad.x, centre.y + rad.y, centre.z + rad.z) * mg,
           c4d.Vector(centre.x - rad.x, centre.y + rad.y, centre.z + rad.z) * mg,
           c4d.Vector(centre.x - rad.x, centre.y - rad.y, centre.z + rad.z) * mg,
           c4d.Vector(centre.x - rad.x, centre.y - rad.y, centre.z - rad.z) * mg,
           c4d.Vector(centre.x + rad.x, centre.y - rad.y, centre.z - rad.z) * mg,
           c4d.Vector(centre.x + rad.x, centre.y + rad.y, centre.z - rad.z) * mg,
           c4d.Vector(centre.x - rad.x, centre.y + rad.y, centre.z - rad.z) * mg,
           c4d.Vector(centre.x + rad.x, centre.y - rad.y, centre.z + rad.z) * mg]

    mini = c4d.Vector(min([p.x for p in pts]), min([p.y for p in pts]), min([p.z for p in pts])) + origine
    maxi = c4d.Vector(max([p.x for p in pts]), max([p.y for p in pts]), max([p.z for p in pts])) + origine

    return mini, maxi


def fichierPRJ(fn):
    fn = os.path.splitext(fn)[0] + '.prj'
    f = open(fn, 'w')
    f.write(
        """PROJCS["CH1903+_LV95",GEOGCS["GCS_CH1903+",DATUM["D_CH1903+",SPHEROID["Bessel_1841",6377397.155,299.1528128]],PRIMEM["Greenwich",0],UNIT["Degree",0.017453292519943295]],PROJECTION["Hotine_Oblique_Mercator_Azimuth_Center"],PARAMETER["latitude_of_center",46.95240555555556],PARAMETER["longitude_of_center",7.439583333333333],PARAMETER["azimuth",90],PARAMETER["scale_factor",1],PARAMETER["false_easting",2600000],PARAMETER["false_northing",1200000],UNIT["Meter",1]]""")
    f.close()


def bbox2shapefile(mini, maxi):
    poly = [[[mini.x, mini.z], [mini.x, maxi.z], [maxi.x, maxi.z], [maxi.x, mini.z]]]

    fn = c4d.storage.LoadDialog(flags=c4d.FILESELECT_SAVE)

    if not fn: return
    with shapefile.Writer(fn, shapefile.POLYGON) as w:
        w.field('id', 'I')
        w.record(1)
        w.poly(poly)

        fichierPRJ(fn)


class DlgBbox(c4d.gui.GeDialog):
    N_MIN = 1015
    N_MAX = 1016
    E_MIN = 1017
    E_MAX = 1018

    BTON_FROM_OBJECT = 1050
    BTON_FROM_VIEW = 1051
    BTON_COPY_ALL = 1052
    BTON_PLANE = 1053
    BTON_EXPORT_SHP = 1054
    BTON_EXTRACT_RASTER = 1061
    BTON_DISPLAY_RASTER = 1062
    BTON_EXTRACT_MNA =1063
    BTON_ORIGIN = 1064

    BTON_N_MIN = 1055
    BTON_N_MAX = 1056
    BTON_E_MIN = 1057
    BTON_E_MAX = 1058

    ID_COMBO_FAMILLE = 1100
    ID_COMBO_SERVER = 1101

    TXT_NO_ORIGIN = "Le document n'est pas géoréférencé !"
    TXT_NOT_VIEW_TOP = "Vous devez activer une vue de haut !"
    TXT_NO_SELECTION = "Vous devez sélectionner un objet !"
    TXT_MULTI_SELECTION = "Vous devez sélectionner un seul objet !"
    TXT_NOT_METER = "Les unités du document ne sont pas en mètres, si vous continuez les unités seront modifiées.\nVoulez-vous continuer ?"

    LST_ORIGIN = [BTON_FROM_OBJECT,BTON_FROM_VIEW,BTON_PLANE,BTON_EXPORT_SHP,BTON_EXTRACT_RASTER,BTON_DISPLAY_RASTER,BTON_EXTRACT_MNA]
    LST_ZERO = [BTON_PLANE,BTON_EXPORT_SHP,BTON_EXTRACT_RASTER,BTON_EXTRACT_MNA,BTON_COPY_ALL,BTON_N_MIN,BTON_N_MAX,BTON_E_MIN,BTON_E_MAX]

    MARGIN = 5
    LARG_COORD = 130

    def CreateLayout(self):
        #pour la mise à jour du dialog
        self.SetTimer(250)

        self.SetTitle("Emprise géographique")

        self.GroupBegin(400, flags=c4d.BFH_CENTER, cols=1, rows=1)
        self.GroupBorderSpace(self.MARGIN, self.MARGIN, self.MARGIN, 0)
        self.GroupSpace(5, 5)

        self.AddButton(self.BTON_ORIGIN, flags=c4d.BFH_MASK, initw=197, inith=20, name="géoréférencement par défaut")

        self.GroupEnd()



        # CADRAGE
        self.GroupBegin(100, flags=c4d.BFH_CENTER, cols=3, rows=1)
        self.GroupBorderSpace(self.MARGIN, self.MARGIN, self.MARGIN, self.MARGIN)
        self.AddStaticText(101, name="N max :", flags=c4d.BFH_MASK, initw=50)
        self.AddEditNumber(self.N_MAX, flags=c4d.BFH_MASK, initw=self.LARG_COORD, inith=0)
        self.AddButton(self.BTON_N_MAX, flags=c4d.BFH_MASK, initw=0, inith=0, name="copier")
        self.GroupEnd()

        self.GroupBegin(200, flags=c4d.BFH_CENTER, cols=7, rows=1)
        self.GroupBorderSpace(self.MARGIN, self.MARGIN, self.MARGIN, self.MARGIN)
        self.AddStaticText(201, name="E min :", flags=c4d.BFH_MASK, initw=50)
        self.AddEditNumber(self.E_MIN, flags=c4d.BFH_MASK, initw=self.LARG_COORD, inith=0)
        self.AddButton(self.BTON_E_MIN, flags=c4d.BFH_MASK, initw=0, inith=0, name="copier")
        self.AddStaticText(202, name="", flags=c4d.BFH_MASK, initw=200)
        self.AddStaticText(203, name="E max :", flags=c4d.BFH_MASK, initw=50)
        self.AddEditNumber(self.E_MAX, flags=c4d.BFH_MASK, initw=self.LARG_COORD, inith=0)
        self.AddButton(self.BTON_E_MAX, flags=c4d.BFH_MASK, initw=0, inith=0, name="copier")
        self.GroupEnd()

        self.GroupBegin(300, flags=c4d.BFH_CENTER, cols=3, rows=1)
        self.GroupBorderSpace(self.MARGIN, self.MARGIN, self.MARGIN, self.MARGIN)
        self.AddStaticText(301, name="N min :", flags=c4d.BFH_MASK, initw=50)
        self.AddEditNumber(self.N_MIN, flags=c4d.BFH_MASK, initw=self.LARG_COORD, inith=0)
        self.AddButton(self.BTON_N_MIN, flags=c4d.BFH_MASK, initw=0, inith=0, name="copier")
        self.GroupEnd()

        self.GroupBegin(400, flags=c4d.BFH_CENTER, cols=2, rows=1)
        self.GroupBorderSpace(self.MARGIN, self.MARGIN, self.MARGIN, 0)
        self.GroupSpace(5, 5)

        self.AddButton(self.BTON_FROM_OBJECT, flags=c4d.BFH_MASK, initw=197, inith=20, name="depuis la sélection")
        self.AddButton(self.BTON_FROM_VIEW, flags=c4d.BFH_MASK, initw=197, inith=20, name="depuis la vue de haut")

        self.GroupEnd()

        self.GroupBegin(500, flags=c4d.BFH_CENTER, cols=3, rows=1)
        self.GroupBorderSpace(self.MARGIN, 0, self.MARGIN,0)
        self.GroupSpace(5, 5)

        self.AddButton(self.BTON_COPY_ALL, flags=c4d.BFH_MASK, initw=120, inith=20, name="copier les valeurs")
        self.AddButton(self.BTON_PLANE, flags=c4d.BFH_MASK, initw=120, inith=20, name="créer un plan")
        self.AddButton(self.BTON_EXPORT_SHP, flags=c4d.BFH_MASK, initw=120, inith=20, name="créer un shapefile")
        self.GroupEnd()

        self.GroupBegin(700, flags=c4d.BFH_LEFT, cols=3, rows=1)
        self.GroupBorderSpace(self.MARGIN, self.MARGIN*4, self.MARGIN, self.MARGIN)
        self.AddStaticText(701, name="Choix du raster :", flags=c4d.BFH_MASK, initw=149)
        self.AddComboBox(self.ID_COMBO_FAMILLE, flags=c4d.BFH_MASK, initw=150)
        self.AddComboBox(self.ID_COMBO_SERVER, flags=c4d.BFH_MASK, initw=350)
        self.GroupEnd()

        self.GroupBegin(600, flags=c4d.BFH_CENTER, cols=3, rows=1)
        self.GroupBorderSpace(self.MARGIN, 0, self.MARGIN, self.MARGIN)
        self.AddButton(self.BTON_DISPLAY_RASTER, flags=c4d.BFH_MASK, initw=120, inith=20, name="ortho vue de haut")
        self.AddButton(self.BTON_EXTRACT_RASTER, flags=c4d.BFH_MASK, initw=120, inith=20, name="extraire un raster")
        self.AddButton(self.BTON_EXTRACT_MNA, flags=c4d.BFH_MASK, initw=120, inith=20, name="extraire un MNA")
        self.GroupEnd()



        return True

    def InitValues(self):
        self.SetMeter(self.N_MAX, 0.0)
        self.SetMeter(self.N_MIN, 0.0)
        self.SetMeter(self.E_MIN, 0.0)
        self.SetMeter(self.E_MAX, 0.0)
        self.UpdateDlg()



        for i,dic in enumerate(api_servers.RASTERS):
            self.AddChild(self.ID_COMBO_FAMILLE, i, dic['famille'])
        self.SetInt32(self.ID_COMBO_FAMILLE,0)
        self.majComboServer()


        return True

    def majComboServer(self):
        self.FreeChildren(self.ID_COMBO_SERVER)
        id = self.GetInt32(self.ID_COMBO_FAMILLE)
        for i,server in enumerate(api_servers.RASTERS[id]['serveurs']):
            self.AddChild(self.ID_COMBO_SERVER, i, server['nom'])
        self.SetInt32(self.ID_COMBO_SERVER,0)
        self.url = self.getURL()

    def getURL(self):
        id_famille = self.GetInt32(self.ID_COMBO_FAMILLE)
        id_server = self.GetInt32(self.ID_COMBO_SERVER)

        return api_servers.RASTERS[id_famille]['serveurs'][id_server]['url']



    def Timer(self, msg) :
        self.UpdateDlg()

    def UpdateDlg(self):
        doc = c4d.documents.GetActiveDocument()
        origin = True
        # si le doc n'est pas géorérérencé
        if not doc[CONTAINER_ORIGIN]: origin = False

        for i in self.LST_ORIGIN:
            self.Enable(i,origin)

        self.Enable(self.BTON_ORIGIN, not origin)

        non_zero = True
        # si on a pas des valeurs
        if not self.GetFloat(self.N_MAX) or not self.GetFloat(self.N_MIN) or not self.GetFloat(self.E_MAX) or not self.GetFloat(self.E_MIN):
            non_zero = False

        for i in self.LST_ZERO:
            self.Enable(i,non_zero)

        #pas d'objet sélectionné ou l'objet n'a pas de geometrie
        obj = doc.GetActiveObject()
        if not obj:
            self.Enable(self.BTON_FROM_OBJECT, False)

        #si la vue active n'est pas une vue de haut
        bd = doc.GetActiveBaseDraw()
        camera = bd.GetSceneCamera(doc)
        if not camera[c4d.CAMERA_PROJECTION] == c4d.Ptop:
            self.Enable(self.BTON_FROM_VIEW, False)
            self.Enable(self.BTON_DISPLAY_RASTER, False)


    def getBbox(self):
        mini = c4d.Vector()
        maxi = c4d.Vector()
        maxi.z = self.GetFloat(self.N_MAX)
        mini.z = self.GetFloat(self.N_MIN)
        maxi.x = self.GetFloat(self.E_MAX)
        mini.x = self.GetFloat(self.E_MIN)
        return mini, maxi

    def planeFromBbox(self, mini, maxi, origine):
        plane = c4d.BaseObject(c4d.Oplane)
        plane[c4d.PRIM_AXIS] = c4d.PRIM_AXIS_YP
        plane[c4d.PRIM_PLANE_SUBW] = 1
        plane[c4d.PRIM_PLANE_SUBH] = 1

        plane[c4d.PRIM_PLANE_WIDTH] = maxi.x - mini.x
        plane[c4d.PRIM_PLANE_HEIGHT] = maxi.z - mini.z

        pos = (mini + maxi) / 2 - origine

        plane.SetAbsPos(pos)
        return plane

    def Command(self, id, msg):

        if id == self.BTON_ORIGIN:
            doc = c4d.documents.GetActiveDocument()
            usdata = doc[c4d.DOCUMENT_DOCUNIT]
            scale, unit = usdata.GetUnitScale()
            if  unit!= c4d.DOCUMENT_UNIT_M:
                rep = c4d.gui.QuestionDialog(self.TXT_NOT_METER)
                if not rep : return True
                unit = c4d.DOCUMENT_UNIT_M
                usdata.SetUnitScale(scale, unit)
                doc[c4d.DOCUMENT_DOCUNIT] = usdata
            doc[CONTAINER_ORIGIN] = ORIGIN_DEFAULT
            c4d.EventAdd()

        # DEPUIS L'OBJET ACTIF
        # TODO : sélection multiple
        if id == self.BTON_FROM_OBJECT:
            doc = c4d.documents.GetActiveDocument()
            origine = doc[CONTAINER_ORIGIN]
            if not origine:
                c4d.gui.MessageDialog(self.TXT_NO_ORIGIN)
                return True
            op = doc.GetActiveObjects(0)
            if not op:
                c4d.gui.MessageDialog(self.TXT_NO_SELECTION)
                return True
            if len(op) > 1:
                c4d.gui.MessageDialog(self.TXT_MULTI_SELECTION)
                return True
            obj = op[0]

            mini, maxi = empriseObject(obj, origine)
            self.SetMeter(self.N_MAX, maxi.z)
            self.SetMeter(self.N_MIN, mini.z)
            self.SetMeter(self.E_MIN, mini.x)
            self.SetMeter(self.E_MAX, maxi.x)

        # DEPUIS LA VUE DE HAUT
        if id == self.BTON_FROM_VIEW:
            doc = c4d.documents.GetActiveDocument()
            origine = doc[CONTAINER_ORIGIN]
            if not origine:
                c4d.gui.MessageDialog(self.TXT_NO_ORIGIN)
                return True

            bd = doc.GetActiveBaseDraw()
            camera = bd.GetSceneCamera(doc)
            if not camera[c4d.CAMERA_PROJECTION] == c4d.Ptop:
                c4d.gui.MessageDialog(self.TXT_NOT_VIEW_TOP)
                return True

            mini, maxi, larg, haut = empriseVueHaut(bd, origine)
            self.SetMeter(self.N_MAX, maxi.z)
            self.SetMeter(self.N_MIN, mini.z)
            self.SetMeter(self.E_MIN, mini.x)
            self.SetMeter(self.E_MAX, maxi.x)

        # COPIER LES VALEURS (et print)
        if id == self.BTON_COPY_ALL:
            n_max = self.GetFloat(self.N_MAX)
            n_min = self.GetFloat(self.N_MIN)
            e_max = self.GetFloat(self.E_MAX)
            e_min = self.GetFloat(self.E_MIN)
            txt = "{0},{1},{2},{3}".format(e_min,n_min,e_max,n_max)
            print(txt)
            c4d.CopyStringToClipboard(txt)

        # CREER UN PLAN
        if id == self.BTON_PLANE:

            mini, maxi = self.getBbox()

            if mini == c4d.Vector(0) or maxi == c4d.Vector(0):
                return True
            doc = c4d.documents.GetActiveDocument()
            doc.StartUndo()
            origine = doc[CONTAINER_ORIGIN]
            if not origine:
                origine = (mini + maxi) / 2
                # pas réussi à faire un undo pour le doc !
                doc[CONTAINER_ORIGIN] = origine

            plane = self.planeFromBbox(mini, maxi, origine)
            doc.AddUndo(c4d.UNDOTYPE_NEW, plane)
            doc.InsertObject(plane)
            doc.EndUndo()
            c4d.EventAdd()

        # EXPORT SHAPEFILE
        if id == self.BTON_EXPORT_SHP:
            mini, maxi = self.getBbox()
            if mini == c4d.Vector(0) or maxi == c4d.Vector(0):
                return True

            bbox2shapefile(mini, maxi)

        # BOUTONS COPIE COORDONNEEs
        if id == self.BTON_N_MIN:
            c4d.CopyStringToClipboard(str(self.GetFloat(self.N_MIN)))

        if id == self.BTON_N_MAX:
            c4d.CopyStringToClipboard(self.GetFloat(self.N_MAX))

        if id == self.BTON_E_MIN:
            c4d.CopyStringToClipboard(str(self.GetFloat(self.E_MIN)))

        if id == self.BTON_E_MAX:
            c4d.CopyStringToClipboard(str(self.GetFloat(self.E_MAX)))


        #AFFICHER RASTER
        if id == self.BTON_DISPLAY_RASTER:
            doc = c4d.documents.GetActiveDocument()

            if verifDocSaved(doc):
                origine = doc[CONTAINER_ORIGIN]
                bd = doc.GetActiveBaseDraw()
                camera = bd.GetSceneCamera(doc)
                mini, maxi, larg, haut = empriseVueHaut(bd, origine)
                path_doc = doc.GetDocumentPath()

                fn_img = getFileName(path_doc, ext='.jpg', prefixe = 'raster')

                if api_raster.extract(self.url,mini,maxi,larg,haut,fn_img, calage = False):
                    modifDisplay(bd,fn_img, mini,maxi,origine)
            #vue_haut.main()

        #EXTRAIRE RASTER
        if id == self.BTON_EXTRACT_RASTER:
            print('BTON_EXTRACT_RASTER')

        #EXTRAIRE MNA
        if id == self.BTON_EXTRACT_MNA:
            mini,maxi = self.getBbox()
            mnt.main(mini.x,mini.z, maxi.x,maxi.z)

        #CHOIX RASTER
        if id == self.ID_COMBO_FAMILLE:
            self.majComboServer()

        if id == self.ID_COMBO_SERVER:
            self.url = self.getURL()
            print(self.url)

        return True

def main():
    dlg = DlgBbox()
    dlg.Open(c4d.DLG_TYPE_ASYNC)


# Execute main()
if __name__ == '__main__':
    dlg = DlgBbox()
    dlg.Open(c4d.DLG_TYPE_ASYNC)