import c4d, os
import shapefile
from glob import glob


CONTAINER_ORIGIN = 1026473

# Script state in the menu or the command palette
# Return True or c4d.CMD_ENABLED to enable, False or 0 to disable
# Alternatively return c4d.CMD_ENABLED|c4d.CMD_VALUE to enable and check/mark
#def state():
#    return True


#parts type
TRIANGLE_STRIP = 0
TRIANGLE_FAN = 1
OUTER_RING = 2
INNER_RING = 3
FIRST_RING = 4
RING = 5

def insert_geotag(obj,origine):
        geotag = c4d.BaseTag(1026472)
        geotag[CONTAINER_ORIGIN] = origine
        obj.InsertTag(geotag)

# Main function
def main():
    path = '/Users/olivier.donze/TEMP/SHP_PRODUIT_CAD_BATI_3D/*.shp'
    res = c4d.BaseObject(c4d.Onull)
    for fn in glob(path):
        print(os.path.basename(fn))

        analys = {}

        with shapefile.Reader(fn) as reader:

            if not reader.shapeType==shapefile.MULTIPATCH:
                print(fn)
                print('pas multipatch')
            #print(reader.fields)

            origin = doc[CONTAINER_ORIGIN]
            if not origin :
                xmin, ymin, xmax, ymax = reader.bbox
                origin = c4d.Vector((xmin+xmax)/2,0,(ymin+ymax)/2)
                doc[CONTAINER_ORIGIN] = origin

            for shp in reader.iterShapes():
                pts = [c4d.Vector(x, z, y)-origin for (x, y), z in zip(shp.points, shp.z)]


                segs = []
                print (shp.parts)
                print (shp.partTypes)
                return
                #pour l'analyse des types de parts rencontrés
                #SITG/bati3D en 2020 uniquement type 2 (OUTER_RING) et 3 (INNER_RING)
                #for partType in shp.partTypes:
                    #n = analys.get(partType,0)
                    #analys[partType] = n+1
                
                for p1,p2 in zip(shp.parts[:-1], shp.parts[1:]):
                    nb_pts = p2-p1
                    segs.append(nb_pts)

                sp = c4d.SplineObject(len(pts),c4d.SPLINETYPE_LINEAR)
                sp.SetAllPoints(pts)

                sp.ResizeObject(len(pts), len(segs))

                for i,cnt in enumerate(segs):
                    sp.SetSegment(i, cnt, closed =True)

                

                sp.Message(c4d.MSG_UPDATE)
                #sp.InsertUnderLast(res)

                
            print(analys)
            print('--------------------------')


    #doc.InsertObject(res)
    c4d.EventAdd()


# Execute main()
if __name__=='__main__':
    main()