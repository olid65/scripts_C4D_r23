import c4d
from c4d import gui
# Welcome to the world of Python


# Script state in the menu or the command palette
# Return True or c4d.CMD_ENABLED to enable, False or 0 to disable
# Alternatively return c4d.CMD_ENABLED|c4d.CMD_VALUE to enable and check/mark
#def state():
#    return True

# Main function
def main():
    poly = doc.GetFirstObject()
    plan = poly.GetNext()
    
    mg = poly.GetMg()
    p1,p2,p3 = [p*mg for p in poly.GetAllPoints()]
    
    dir1 = (p2-p1).GetNormalized()
    dir2 = (p3-p1).GetNormalized()
    
    v2 = dir1.Cross(dir2)
    v3 = dir1
    v1 = v3.Cross(v2)
    off = p1
    
    
    mg = c4d.Matrix(off,v1,v2,v3)
    plan.SetMg(mg)
    c4d.EventAdd()

# Execute main()
if __name__=='__main__':
    main()