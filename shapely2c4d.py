import c4d,sys

sys.path.append('/Users/olivier.donze/opt/anaconda3/lib/python3.8/site-packages')
from shapely.geometry import LineString
from shapely.ops import polygonize_full

def vectorToList(v):
    return [v.x,v.z]

def listToVector(lst):
    if len(lst)==2:
        x,z = lst
        v = c4d.Vector(x,0,z)
    elif len(lst)==3:
        x,z,y = lst
        v =  c4d.Vector(x,y,z)
    else:
        v = None
    return v
    
def splineToLineString(sp):
    mg = sp.GetMg()
    
    pts = [vectorToList(p*mg) for p in sp.GetAllPoints()]

    # si la spline est fermée on rajoute lée premier point à la fin
    if sp.IsClosed():
        pts.append(pts[0])
    
    return LineString(pts)

def lineStringToSpline(ls):
    pts = [listToVector(p) for p in ls.coords]
    sp = c4d.SplineObject(len(pts),c4d.SPLINETYPE_LINEAR)
    sp.SetAllPoints(pts)
    sp.Message(c4d.MSG_UPDATE)
    return sp

# Main function
def main():
    
    lines = [ splineToLineString(sp) for sp in op.GetChildren()]
    
    result, dangles, cuts, invalids  = polygonize_full(lines)
    
    if not result.is_empty:
        print(result)
        
    if not dangles.is_empty:
        print(dangles)
        
    if not cuts.is_empty:
        cuts_null = c4d.BaseObject(c4d.Onull)
        cuts_null.SetName("cuts")
        for line in cuts:
            sp = lineStringToSpline(line)
            sp.InsertUnderLast(cuts_null)
        doc.InsertObject(cuts_null)
        
    if not invalids.is_empty:
        print(invalids)
    c4d.EventAdd()




# Execute main()
if __name__=='__main__':
    main()