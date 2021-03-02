import c4d

ID_EGID_BC = 1030877
ECHELLE_MNT = 0
ECHELLE_BAT = 1


def getIdsPtsFromPoly(poly):
    return [poly.a,poly.b,poly.c,poly.d]

def getIdsPts(id_poly_dprt,nb_poly,o):
    ids = []
    for i in range(id_poly_dprt,id_poly_dprt+nb_poly):
        ids+=getIdsPtsFromPoly(o.GetPolygon(i))
    ids.sort()
    return ids[0],ids[-1]

def ptScale(pt,base):
    dif_haut = (pt.y-base)*(ECHELLE_BAT-1)
    p = c4d.Vector(pt.x,pt.y-base + base *ECHELLE_MNT + dif_haut,pt.z)
    return p


def main():
    bc = op[ID_EGID_BC]
    nb_bati = bc[0]
    bc2 = bc.GetContainer(1)
    pts = []
    for i in range(nb_bati):
        bc3 = bc2.GetContainer(i)
        id_poly_dprt = bc3[0]
        nb_poly = bc3[1]
        no_egid = bc3[2]
        id_pt_dprt, id_pt_fin = getIdsPts(id_poly_dprt,nb_poly,op)

        pts_temp = [op.GetPoint(i) for i in range(id_pt_dprt,id_pt_fin+1)]
        base = min([p.y for p in pts_temp])

        pts += [ptScale(pt,base) for pt in pts_temp]

    doc.StartUndo()
    doc.AddUndo(c4d.UNDOTYPE_CHANGE,op)
    op.SetAllPoints(pts)
    op.Message(c4d.MSG_UPDATE)
    doc.EndUndo()
    c4d.EventAdd()

if __name__=='__main__':
    main()