import c4d, math


def polygonizeSpline(sp):
    #on passe par SplineHelp pour la fonction GetLineObject
    #sinon on ne peut pas parmétrer les segement en créant directe4ment un LineObject
    sph = c4d.utils.SplineHelp()
    sph.InitSplineWith(sp, flags=c4d.SPLINEHELPFLAGS_RETAINLINEOBJECT)
    lineObject = sph.GetLineObject()
    
    #Triangulation
    poly = lineObject.Triangulate(0.0)
    
    #"Détriangulation" pour obtenir des ngons
    bc = c4d.BaseContainer()
    bc[c4d.MDATA_UNTRIANGULATE_NGONS] = True #pour faire des ngons
    bc[c4d.MDATA_UNTRIANGULATE_ANGLE_RAD] = math.pi/180. #correspond à 1°
    
    res = c4d.utils.SendModelingCommand(command=c4d.MCOMMAND_UNTRIANGULATE,
                                list=[poly],
                                mode=c4d.MODELINGCOMMANDMODE_POLYGONSELECTION,
                                bc=bc,
                                doc=doc)
    if res :
        return poly
    else:
        return False

def main():
    poly = polygonizeSpline(op)
    doc.InsertObject(poly)
    c4d.EventAdd()

# Execute main()
if __name__=='__main__':
    main()