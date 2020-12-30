import c4d
from c4d import gui
# Welcome to the world of Python


# Script state in the menu or the command palette
# Return True or c4d.CMD_ENABLED to enable, False or 0 to disable
# Alternatively return c4d.CMD_ENABLED|c4d.CMD_VALUE to enable and check/mark
#def state():
#    return True




def area2Dpoly(pts):
    """calcule la surface planaire (x,z) d'un polygone 
       d'après https://www.mathopenref.com/coordpolygonarea2.html"""
    area = 0
    j = len(pts)-1
    for i in range(len(pts)):
        area +=  (pts[j].x+pts[i].x) * (pts[j].z-pts[i].z)
        j = i
    return area/2.

def area2Dpolyobj(poly_obj):
    area = 0
    mg = poly_obj.GetMg()
    pts = [p*mg for p in poly_obj.GetAllPoints()]
    polys = poly_obj.GetAllPolygons()
    
    for poly in polys:
        p1 = pts[poly.a]
        p2 = pts[poly.b]
        p3 = pts[poly.c]
        p4 = pts[poly.d]

        
        if p3 == p4:
            area+=area2Dpoly([p1,p2,p3])
        else:
            area+=area2Dpoly([p1,p2,p3,p4])
        
    return area

def area2Dspline(sp):
    """Attention ne fonctionne pas avec une spline trouée"""
    
    mg = sp.GetMg()
    pts = [p*mg for p in sp.GetAllPoints()]
    return area2Dpoly(pts)
    
    
    


def main():
    #print(area2Dpolyobj(op))
    print(area2Dspline(op))

# Execute main()
if __name__=='__main__':
    main()
    
    
