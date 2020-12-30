import c4d
from c4d import gui


# Script state in the menu or the command palette
# Return True or c4d.CMD_ENABLED to enable, False or 0 to disable
# Alternatively return c4d.CMD_ENABLED|c4d.CMD_VALUE to enable and check/mark
#def state():
#    return True

DELTA_ALT = 10 #marge de sécurité pour altitude (utilisé dans getMinMax) 
SUFFIX_EXTRACT = "_extrait"


def getMinMaxY(obj):
    mg = obj.GetMg()
    alt = [(pt*mg).y for pt in obj.GetAllPoints()]
    return min(alt)-DELTA_ALT, max(alt)+DELTA_ALT

def changeAltAbs(pt, mg, alt):
    pt = pt*mg
    pt.y = alt
    return pt *~mg

def volumeFromSpline(sp,minY,maxY):
    
    mg = sp.GetMg()
    
    #on met les points de la spline au minY
    pts = [changeAltAbs(p, mg, minY) for p in sp.GetAllPoints()]
    sp.SetAllPoints(pts)
    sp.Message(c4d.MSG_UPDATE)
    
    #extrusion
    extr = c4d.BaseObject(c4d.Oextrude)
    extr[c4d.EXTRUDEOBJECT_DIRECTION] = c4d.EXTRUDEOBJECT_DIRECTION_Y
    extr[c4d.EXTRUDEOBJECT_EXTRUSIONOFFSET] = maxY-minY
    sp.InsertUnder(extr)
    return extr

def cutMNTfromSpline(mnt,sp):
    """extract the part of mnt wich intesect wit spline (only in Y axis) """
    sp_clone = sp.GetClone()
    
    #calculation of altitude min and max from terrain (avec security margin)
    minY,maxY = getMinMaxY(mnt)
    
    #volume from spline for extraction    
    extr = volumeFromSpline(sp_clone,minY,maxY)
    
    #boolean
    boolObj = c4d.BaseObject(c4d.Oboole)
    boolObj[c4d.BOOLEOBJECT_TYPE] = c4d.BOOLEOBJECT_TYPE_INTERSECT
    boolObj[c4d.BOOLEOBJECT_HIGHQUALITY] = False
    
    extr.InsertUnder(boolObj)
    mnt.GetClone().InsertUnder(boolObj)
    
    
    #temporary file
    temp_doc = c4d.documents.BaseDocument()   
    
    mnt_extract = None
    #TODO : manage exceptions if not ...
    if temp_doc:
        temp_doc.InsertObject(boolObj)
        temp_doc_polygonize = temp_doc.Polygonize()
        bool_res = temp_doc_polygonize.GetFirstObject()
        
        if bool_res:
            mnt_extract = bool_res.GetDown()
            
            if mnt_extract:
                mnt_extract.SetName(mnt.GetName()+SUFFIX_EXTRACT)
    
    return mnt_extract.GetClone()

def clonerFromPolyObject(poly_object,obs_to_clone):
    pass

# Main function
def main():
    sp = doc.GetFirstObject()
    mnt = sp.GetNext()
    
    mnt_extract = cutMNTfromSpline(mnt,sp)

    if mnt_extract : doc.InsertObject(mnt_extract.GetClone(), pred = mnt)
    c4d.EventAdd()

# Execute main()
if __name__=='__main__':
    main()