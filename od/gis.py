# -*- coding: utf-8 -*-

import c4d
from od_const import CONTAINER_ORIGIN

ID_GEOTAG = 1026472

#GEOREFERENCEMENT

def isGeoref(obj):
    """renvoie True si l'objet a déjà un GeoTag"""
    t = obj.GetFirstTag()
    while t:
        if t.CheckType(ID_GEOTAG) :
            return True
        t = t.GetNext()
    return False

def georefObj(obj,doc):
    if isGeoref(obj) : return
    tg = c4d.BaseTag(ID_GEOTAG)
    pos = obj.GetAbsPos()
    tg[CONTAINER_ORIGIN] = doc[CONTAINER_ORIGIN]+pos
    obj.InsertTag(tg)
    doc.AddUndo(c4d.UNDOTYPE_NEW,tg)

