# -*- coding: utf-8 -*-

import c4d
from libs import shapefile
import os

CONTAINER_ORIGIN = 1026473



def testShape(fn):
    # on regarde si l'extension est la bonne
    if os.path.splitext(fn)[1] == '.shp': return True
    return False

def shpPoly2spline(shp,centre,hasZ = False):
    pts = []
    if hasZ:
        pts = [c4d.Vector(x, z, y) - centre for (x, y), z in zip(shp.points, shp.z)]
    else:
        pts = [c4d.Vector(x, 0, y) - centre for x, y in shp.points]
    nb_pts = len(pts)
    sp = c4d.SplineObject(nb_pts, c4d.SPLINETYPE_LINEAR)
    sp[c4d.SPLINEOBJECT_CLOSED] = True
    sp.SetAllPoints(pts)

    # SEGMENTS
    nb_seg = len(shp.parts)
    if nb_seg > 1:
        sp.ResizeObject(nb_pts, nb_seg)
        shp.parts.append(nb_pts)
        segs = [fin - dbt for dbt, fin in zip(shp.parts[:-1], shp.parts[1:])]
        for i, n in enumerate(segs):
            sp.SetSegment(i, n, closed=True)
    sp.Message(c4d.MSG_UPDATE)
    return sp


def splinesFromShapefile(fn,origine):

    reader = shapefile.Reader(fn)

    hasZ = False

    if reader.shapeType == shapefile.POLYGON:
        hasZ = False
    elif reader.shapeType == shapefile.POLYGONZ:
        hasZ = True
    else :
        c4d.gui.MessageDialog("Ce n'est pas un fichier de type polygone")
        return

    splines = []

    for shp in reader.iterShapes():
        splines.append(shpPoly2spline(shp,origine,hasZ))

    return splines


# Main function
def main(fn=None,
         fn_arbres='/Users/olivier.donze/Library/Preferences/MAXON/Maxon Cinema 4D R23_2FE1299C/plugins/SITG_C4D/__arbres_2018__.c4d'):

    #récupération du MNT
    doc = c4d.documents.GetActiveDocument()
    mnt = doc.GetActiveObject()

    if not mnt or not mnt.CheckType(c4d.Opolygon) :
        c4d.gui.MessageDialog("Vous devez sélectionner un terrain (objet polygonal) sur lequel les zones vont être plantées")
        return

    #Verification du georeferencement du fichier
    origine = doc[CONTAINER_ORIGIN]
    if not origine:
        c4d.gui.MessageDialog("Le document n'est pas géoréférencé, opération impossible !")
        return


    #SHAPEFILE polygones
    #fn = c4d.storage.LoadDialog(type=c4d.FILESELECTTYPE_IMAGES, title="Séléctionnez le fichier .shp :")
    fn = '/Users/olivier.donze/TEMP/LaPage_modele_donnees/PP_ARBRE_S.shp'
    if not fn: return

    if not testShape(fn):
        c4d.gui.MessageDialog("Ce n'est pas un fichier shape (.shp)")
        return

    splines = splinesFromShapefile(fn, origine)

if __name__ == '__main__':
    main()