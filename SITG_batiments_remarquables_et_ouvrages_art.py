import c4d,os, shutil
from glob import glob

#à modifier si on veut ou pas les materiaux
# peut ^être lourd et long car copie toutes les texture dans tex
MATERIAUX = False

CONTAINER_ORIGIN =1026473

OA_OFFSET_FILE_NAME = 'Offset_OA.txt'

NOT_SAVED_TXT = "Le document doit être enregistré pour pouvoir copier les textures dans le dossier tex, vous pourrez le faire à la prochaine étape\nVoulez-vous continuer ?"

DIRNAME_OA = 'bat_remarquables_et_ouvrages_art'

OUVRAGES_ART_NAME = "ouvrages_art"

BATI_REMARQUABLES_NAME = "batiments_remarquables"

DOC_NOT_IN_METERS_TXT = "Les unités du document ne sont pas en mètres, si vous continuez les unités seront modifiées.\nVoulez-vous continuer ?"

OUVRAGES_ART_LYR_COLOR = c4d.Vector(1,0,0)

BATI_REMARQUABLES_COLOR = c4d.Vector(1,1,0)

def getLayerByName(name,doc):
    """si le layer existe le renvoie sinon renvoie None
    Attention seulement au premier niveau, j'ai pas réussi à régler la récursion"""
    layer=doc.GetLayerObjectRoot().GetDown()
    while layer:
        if name == layer.GetName(): return layer
        layer = layer.GetNext()
    return None

def layerByName(name,doc, color = None):
    """renvoie le layer s'il existe
       sinon il le cree et le renvoie"""
    layer = getLayerByName(name,doc)

    if not layer :
        layer =c4d.documents.LayerObject()
        layer.SetName(name)
        parent = doc.GetLayerObjectRoot()
        layer.InsertUnder(parent)
    if color :
        data = layer.GetLayerData(doc)
        data['color'] = color
        layer.SetLayerData(doc,data)
    return layer


def readFWT(fn):
    """lecture du fichier fwt des b^âtiments remarquables
       cela semble être une matrice 4x4
       il ne semble pas avoir de rotation, mais juste une mise à l'échelle
       donc je n'ai pas tenu compte des rotations éventuelles

       renvoie les vecteurs de translation et d'échelle"""
    try :
        with open(fn) as f:
            fwt = f.read().split()
            scalex = float(fwt[0])/100
            transx = float(fwt[3])
            scalez = float(fwt[5])/100
            transz = float(fwt[7])
            scaley = float(fwt[10])/100
            transy = float(fwt[11])

            scale = c4d.Vector(scalex,scaley,scalez)*100
            translation = c4d.Vector(transx,transy,transz)
    except : return False

    return translation,scale

def getFilesFromDir(pth,ext =''):
    return glob(os.path.join(pth,'*'+ext))

def getFilesFromDir_recursive(pth,ext =''):
    res = []
    if os.path.isdir(pth): res.extend(getFilesFromDir(pth,ext))

    for pth2 in glob(os.path.join(pth,'*')):
        if os.path.isdir(pth2):
            res.extend(getFilesFromDir_recursive(pth2,ext))
    return res

def read_OA_Offset(fn):
    with open(fn) as f :
        transx = float(f.readline().split()[-1])
        transz = float(f.readline().split()[-1])
        return c4d.Vector(transx,0,transz)

def merge3ds(fn_3ds,doc, lyrname):

    first_obj = doc.GetFirstObject()
    first_mat = doc.GetFirstMaterial()

    dir_up,name = os.path.split(fn_3ds)
    name = os.path.basename(dir_up)


    if MATERIAUX :
        lyr = layerByName(lyrname,doc)
        path_tex = os.path.join(doc.GetDocumentPath(),'tex',DIRNAME_OA)

        if not os.path.isdir(path_tex):
            os.makedirs(path_tex)
        dic_png = {}

        #copie des png
        for fn_png in glob(os.path.join(dir_up,'*.png')):
            dir_png,old_name_png = os.path.split(fn_png)
            new_name_png = name+'_'+old_name_png
            dic_png[old_name_png] = new_name_png
            new_fn_png = os.path.join(path_tex,new_name_png)

            #TODO gérer si le fichier existe !
            if os.path.isfile(new_fn_png) :
                print(f"le fichier '{new_name_png}' existe déjà")
            else:
                shutil.copy(fn_png, new_fn_png)


    #merge des documents
    res = c4d.BaseObject(c4d.Onull)
    res.SetName(name)

    if MATERIAUX:
        c4d.documents.MergeDocument(doc, fn_3ds, c4d.SCENEFILTER_OBJECTS|c4d.SCENEFILTER_MATERIALS,None)
    else:
        c4d.documents.MergeDocument(doc, fn_3ds, c4d.SCENEFILTER_OBJECTS,None)


    objs = []
    obj = doc.GetFirstObject()

    while obj != first_obj:
        if obj!= res:
            objs.append(obj)
        obj = obj.GetNext()
    for o in objs :
        o.InsertUnder(res)

    if MATERIAUX :
        mat = doc.GetFirstMaterial()

        while mat != first_mat:
            mat[c4d.ID_LAYER_LINK] = lyr
            mat.SetName(name+'_'+mat.GetName())
            shader = getBMPshader(mat)
            if shader :
                old = shader[c4d.BITMAPSHADER_FILENAME]
                new = dic_png.get(old, None)
                if new :
                    shader[c4d.BITMAPSHADER_FILENAME] = new
                    mat.Message(c4d.MSG_UPDATE)
                    mat.Update(True, True)

            mat = mat.GetNext()
            
            #TODO :si transparence -> ajouter dans le canal alpha
            #bmp = c4d.bitmaps.BaseBitmap()
            #bmp.InitWith(fn)
            #transp = bmp.GetInternalChannel()
            #if transp:
                #ajouter dans canal alpha l'image
    return res

def getBMPshader(mat):
    shader = mat.GetFirstShader()
    while shader:
        if shader.CheckType(c4d.Xbitmap):
            return shader
        shader = shader.GetNext()
    return None




# Main function
def main():

    #TODO : il faut que le doc soit en mètres
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

    path = None
    path = '/Users/donzeo/Documents/Mandats/SITG/format_z_3D_3DS_OUVRAGES_canton_all_20210113_134339'
    #path = '/Users/donzeo/Documents/Mandats/SITG/format_z_3D_3DS_OUVRAGES_canton_all_20210113_134339/12_quai_du_Rhone'
    #path = '/Users/donzeo/Documents/Mandats/SITG'
    if not path :
        path = c4d.storage.LoadDialog(flags=c4d.FILESELECT_DIRECTORY, title='')
    if not path : return

    origin = doc[CONTAINER_ORIGIN]

    res_OA = None
    res_BatiRem = None

    #recuperation de tous les fichier 3ds
    for fn_3ds in getFilesFromDir_recursive(path,ext ='.3ds'):



        dir_up,name = os.path.split(fn_3ds)
        name = os.path.basename(dir_up)

        fn_offset = os.path.join(dir_up,OA_OFFSET_FILE_NAME)

        #fichier calage pour les bati remarquables
        fn_fwt = fn_3ds.replace('.3ds','.fwt')

        #BATIMENTS REMARQUABLES
        if os.path.isfile(fn_fwt):
            if not res_BatiRem :
                res_BatiRem = c4d.BaseObject(c4d.Onull)
                res_BatiRem.SetName(BATI_REMARQUABLES_NAME)
                #layer
                res_BatiRem[c4d.ID_LAYER_LINK] = layerByName(BATI_REMARQUABLES_NAME,doc, color = BATI_REMARQUABLES_COLOR)

            #merge du fichier 3ds avec le fichier courant
            obj_null = merge3ds(fn_3ds,doc,BATI_REMARQUABLES_NAME)
            obj_null.InsertUnderLast(res_BatiRem)
            trans,scale = readFWT(fn_fwt)

        #OUVRAGE ART
        #sinon on regarde si on a un fichier Offset_OA.txt pour les ouvrages d'art'
        elif os.path.isfile(fn_offset) :

            if not res_OA :
                res_OA = c4d.BaseObject(c4d.Onull)
                res_OA.SetName(OUVRAGES_ART_NAME)
                #layer
                res_OA[c4d.ID_LAYER_LINK] = layerByName(OUVRAGES_ART_NAME,doc, color = OUVRAGES_ART_LYR_COLOR)

            #merge du fichier 3ds avec le fichier courant
            obj_null = merge3ds(fn_3ds,doc,OUVRAGES_ART_NAME)
            obj_null.InsertUnderLast(res_OA)


            trans = read_OA_Offset(fn_offset)
            scale = c4d.Vector(1)

        if not origin :
            doc[CONTAINER_ORIGIN] = trans
            origin = doc[CONTAINER_ORIGIN]

        obj_null.SetAbsPos(trans-origin)

        #TODO : modifier la géométrie plutôt que l'échelle'
        obj_null.SetAbsScale(scale)

    if res_BatiRem:
        doc.InsertObject(res_BatiRem)
    if res_OA:
        doc.InsertObject(res_OA)

    c4d.EventAdd()

# Execute main()
if __name__=='__main__':
    main()