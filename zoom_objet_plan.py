import c4d

SCALE = 5000
RES = 300 #pixel/pouce

#TODO tenir compte si on est en cm ou m !!!!!!

def GetCamera(doc):
    """
    Returns the active camera.
    Will never be None.
    """
    bd = doc.GetRenderBaseDraw()
    cp = bd.GetSceneCamera(doc)
    if cp is None: cp = bd.GetEditorCamera()

    return cp

def main():

    #calcul de la taille de l'objet sélectionné
    mg = op.GetMg()
    centre = op.GetMp() *mg
    rad = op.GetRad()
    taille_objet = c4d.Vector(rad.x*2,0,rad.z*2)

    render_size = (taille_objet / SCALE *100)/2.54 *RES
    print (render_size)
    rd = doc.GetActiveRenderData()
    rd[c4d.RDATA_XRES] = int(round(render_size.x))
    rd[c4d.RDATA_YRES]= int(round(render_size.z))
    rd[c4d.RDATA_PIXELRESOLUTION] = RES

    cam = GetCamera(doc)
    cam.SetAbsPos(centre)

    bd = doc.GetRenderBaseDraw()

    #recuperation des donnes de la vue pour la taille de la zone
    position = bd.GetSafeFrame()
    left, top, right, bottom = position["cl"], position["ct"], position["cr"], position["cb"]
    larg_fen = (right-left)
    ht_fen = bottom-top
    #calcul de l'echelle souhaitee entre le monde et la vue
    scaleX = larg_fen/taille_objet.x

    cam[c4d.CAMERA_ZOOM] = scaleX/larg_fen*1024
    cam.Message(c4d.MSG_UPDATE)
    bd.Message(c4d.MSG_UPDATE)
    rd.Message(c4d.MSG_UPDATE)
    c4d.EventAdd()


if __name__=='__main__':
    main()