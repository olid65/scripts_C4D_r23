import c4d
import shapefile

CONTAINER_ORIGIN = 1026473

def fusionSplines(lst_sp, nom = None, closed = True):
    """fusionne toute les splines de la liste en une seule en une"""
    pts = []
    nb_seg = 0
    seg = []
    
    for sp in lst_sp:
        mg = sp.GetMg()
        pts.extend([p*mg for p in sp.GetAllPoints()])
        if sp.GetSegmentCount():
            for id in range(sp.GetSegmentCount()):
                seg.append(sp.GetSegment(id)['cnt'])
                nb_seg+=1
        else :
            seg.append(sp.GetPointCount())
            nb_seg+=1
    
    nb_pts = sum([s.GetPointCount() for s in lst_sp])
    res = c4d.SplineObject(nb_pts, c4d.SPLINETYPE_LINEAR)
    if nom : res.SetName(nom)
    res[c4d.SPLINEOBJECT_CLOSED] = closed
    res.ResizeObject(nb_pts,nb_seg)
    res.SetAllPoints(pts)

    for id,cnt in enumerate(seg):
        res.SetSegment(id,cnt,closed = closed)
        
    res.Message(c4d.MSG_UPDATE)
    return res

def getPts(shp, origin, hasZ = False):
    if hasZ:
        return [c4d.Vector(x, z, y) - origin for (x, y), z in zip(shp.points, shp.z)]
    else:
        return [c4d.Vector(x, 0, y) - origin for x, y in shp.points]


def shp2splines(fn, origin):
    """renvoie une liste de splines multisegments"""
    res = []

    with shapefile.Reader(fn) as reader :
        if reader.shapeType not in [shapefile.POLYLINE, shapefile.POLYGON,shapefile.POLYLINEZ, shapefile.POLYGONZ]:
            return False
        
        if not origin:
            xmin,ymin,xmax,ymax = reader.bbox
            origin = c4d.Vector((xmin+ymin)/2,0,(xmax+ymax)/2)
            doc = c4d.documents.GetActiveDocument()
            doc[CONTAINER_ORIGIN] = origin

        closed = False
        if reader.shapeType in [shapefile.POLYGON, shapefile.POLYGONZ]:
            closed = True

        hasZ = False
        if reader.shapeType in [shapefile.POLYLINEZ, shapefile.POLYGONZ]:
            hasZ = True

        for shp in reader.iterShapes():
            pts = getPts(shp, origin, hasZ)
            nb_pts = len(pts)
            sp = c4d.SplineObject(nb_pts, c4d.SPLINETYPE_LINEAR)
            sp.SetAllPoints(pts)
            # SEGMENTS
            nb_seg = len(shp.parts)
            if nb_seg > 1:
                sp.ResizeObject(nb_pts, nb_seg)
                shp.parts.append(nb_pts)
                segs = [fin - dbt for dbt, fin in zip(shp.parts[:-1], shp.parts[1:])]
                for i, n in enumerate(segs):
                    sp.SetSegment(i, n, closed=closed)
            sp[c4d.SPLINEOBJECT_CLOSED] = closed
            sp.Message(c4d.MSG_UPDATE)
            res.append(sp)
    return res

def shp2instances(fn,origin,sources):
    """renvoie une liste d'instances"""
    pass

def shp2multiinstance(fn,origin,sources):
    """renvoie un objet multiinstance par objet source avec tous les points"""
    pass

def shp2cloner(fn,origin,sources):
    """renvoie un neutre avec en enfant un objet point pour les positions
       et un cloner en mode objet"""
    pass

def shp2polygon(fn,origin):
    """renvoie une liste d'objets polygonaux (un par entité)
       depuis un multipatch ou polygone 3D"""
    pass

def main():
    fn = '/Users/olivier.donze/Mandats/Penetrantes_vertes_2021/SIG/isoligne_poly_mnt20m_Simplif_lissage100m.shp'
    origin = doc[CONTAINER_ORIGIN]

    splines = shp2splines(fn, origin)
    sp = fusionSplines(splines, nom = None, closed = True)

    doc.InsertObject(sp)
    c4d.EventAdd()


if __name__ == "__main__":
    main()