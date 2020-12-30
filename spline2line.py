import c4d
from c4d import gui
# Welcome to the world of Python


# Script state in the menu or the command palette
# Return True or c4d.CMD_ENABLED to enable, False or 0 to disable
# Alternatively return c4d.CMD_ENABLED|c4d.CMD_VALUE to enable and check/mark
#def state():
#    return True



def spline2line(sp):
    """converti un spline fermée multisegment
       en polyligne o(spline ouverte"""
       
    res = sp.GetClone()
    res[c4d.SPLINEOBJECT_CLOSED]=False
    mg = sp.GetMg()
    nb_pts = sp.GetPointCount()
    pts = res.GetAllPoints()
    
    nb_segments = sp.GetSegmentCount()
    
    #spline monosegment
    if nb_segments<2:
        res.ResizeObject(nb_pts+1)
        new_p = c4d.Vector(pts[0].x,pts[0].y,pts[0].z)
        pts.append(new_p)
    #spline multisegment
    else:
        res.ResizeObject(nb_pts+nb_segments)
        id_pt  = 0
        for i in range(nb_segments):
            segment = spline.GetSegment(i)
            new_p = c4d.Vector(pts[id_pt].x,pts[id_pt].y,pts[id_pt].z)]
            
            cnt = segment["cnt"]

        
    
    
    res.SetAllPoints(pts)
    res.SetMg(mg)
    res.Message(c4d.MSG_UPDATE)
    return res
        
        

# Main function
def main():
    sp = spline2line(op)
    doc.InsertObject(sp)
    c4d.EventAdd()
# Execute main()
if __name__=='__main__':
    main()