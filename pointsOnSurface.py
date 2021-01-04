
import c4d

"""Projette verticalement les points de l'objet polygonal sélectionné (ou de la spline)
   sur l'objet polygonal juste apres dans la hiérarchie
   Ne fonctionne pas avec les primitives"""
   
DELTA_ALT = 100
   
def getMinMaxY(obj):
    """renvoie le minY et le maxY en valeur du monde d'un objet"""
    mg = obj.GetMg()
    alt = [(pt * mg).y for pt in obj.GetAllPoints()]
    return min(alt) - DELTA_ALT, max(alt) + DELTA_ALT
   
def pointsOnSurface(op,mnt):
    grc = c4d.utils.GeRayCollider()
    grc.Init(mnt)

    mg_op = op.GetMg()
    mg_mnt = mnt.GetMg()
    invmg_mnt = ~mg_mnt
    invmg_op = ~op.GetMg()
    
    minY,maxY = getMinMaxY(mnt)
    
    ray_dir = ((c4d.Vector(0,0,0)*invmg_mnt) - (c4d.Vector(0,1,0)*invmg_mnt)).GetNormalized()
    length = maxY-minY
    for i,p in enumerate(op.GetAllPoints()):
        p = p*mg_op
        dprt = c4d.Vector(p.x,maxY,p.z)*invmg_mnt
        intersect = grc.Intersect(dprt,ray_dir,length)
        if intersect :
            pos = grc.GetNearestIntersection()['hitpos']
            op.SetPoint(i,pos*mg_mnt*invmg_op)
    
    op.Message(c4d.MSG_UPDATE)

def main():
    if not op :
        c4d.gui.MessageDialog("""Vous devez sélectionner un seul objet polygonal ou une spline""")
        return
    if not (op.CheckType(c4d.Opolygon) or  op.CheckType(c4d.Ospline)):
        c4d.gui.MessageDialog("""L'objet sélectionné doit être un objet polygonal ou une spline""")
        return
    mnt = op.GetNext()
    if not mnt or not mnt.CheckType(c4d.Opolygon):
        c4d.gui.MessageDialog("""L'objet suivant doit être un objet polygonal""")
        return
    doc.StartUndo()
    doc.AddUndo(c4d.UNDOTYPE_CHANGE,op)
    pointsOnSurface(op,mnt)
    doc.EndUndo()
    c4d.EventAdd()
    return

if __name__=='__main__':
    main()