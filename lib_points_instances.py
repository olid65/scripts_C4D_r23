import c4d, math
from random import random


# Script state in the menu or the command palette
# Return True or c4d.CMD_ENABLED to enable, False or 0 to disable
# Alternatively return c4d.CMD_ENABLED|c4d.CMD_VALUE to enable and check/mark
#def state():
#    return True


def multiInstanceFromPoints(pts,obj_ref = None):
    inst = c4d.BaseObject(c4d.Oinstance)
    inst[c4d.INSTANCEOBJECT_RENDERINSTANCE_MODE] = c4d.INSTANCEOBJECT_RENDERINSTANCE_MODE_MULTIINSTANCE
    inst[c4d.INSTANCEOBJECT_LINK] =obj_ref
    
    matrices = []
    
    for pt in pts() :
        m = c4d.Matrix()
        m.off = pt
        matrices.append(m)
    return inst

def polygonObjectFromPoints(pts):
    polyo = c4d.PolygonObject(len(pts),0)
    polyo.SetAllPoints(pts)
    polyo.Message(c4d.MSG_UPDATE)
    return polyo
    
def multiInstanceFromPolygonObject(poly,obj_ref = None):
    inst = c4d.BaseObject(c4d.Oinstance)
    inst[c4d.INSTANCEOBJECT_RENDERINSTANCE_MODE] = c4d.INSTANCEOBJECT_RENDERINSTANCE_MODE_MULTIINSTANCE
    inst[c4d.INSTANCEOBJECT_LINK] =obj_ref
    
    inst[c4d.INSTANCEOBJECT_MULTIPOSITIONINPUT]=obj_ref
    return inst

def clonerFromPoints(pts,objs_ref =[]):
    poly = polygonObjectFromPoints(pts)
    
    pass
    
    

# Main function
def main():
    new_m =[]
    for m in op.GetInstanceMatrices():
        angle = random()*math.pi*2
        mrot = c4d.utils.MatrixRotY(angle)
        new_m.append(m *mrot)
    op.SetInstanceMatrices(new_m)    
    c4d.EventAdd()
    return
    
    inst = c4d.BaseObject(c4d.Oinstance)
    inst[c4d.INSTANCEOBJECT_RENDERINSTANCE_MODE] = c4d.INSTANCEOBJECT_RENDERINSTANCE_MODE_MULTIINSTANCE
    inst[c4d.INSTANCEOBJECT_LINK] =op
    
    nb_clone = 100
    dist = 1000
    
    matrices = []
    for i in range(nb_clone):
        m = c4d.Matrix()
        pos = c4d.Vector(random()*dist,random()*dist,random()*dist)
        print(pos)
        m.off = pos
        matrices.append(m)
    inst.SetInstanceMatrices(matrices)
    doc.InsertObject(inst)
    c4d.EventAdd()
    
    
# Execute main()
if __name__=='__main__':
    main()