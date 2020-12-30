import c4d
from c4d import gui



TXT_NO_SPLINE = "Vous devez sélectionner au moins une spline ou un objet neutre contenant des splines !"
TXT_CHECK_SPLINE = "Il y a une ou plusieurs splines qui ne sont soit pas fermées soit qui possèdent moins que 3 points.\nVoulez-vous continuer ?"
TXT_NO_POLYOBJECT = "Vous devez sélectionner également un objet polygonal (terrain)"
TXT_MANY_POLYOBJECT = "Il y a plusieurs objets polygonaux sélectionné, le premier ({}) sera utilisé comme terrain.\nVoulez-vous continuer?"


def checkSpline(splines):
    for sp in splines:
        if not sp.IsClosed() : return False
        #s'il n'y a pas au moins 3 points on renvoie false
        if sp.GetPointCount()<3 : return False
    return True

# Main function
def getSplinesAndMNT():
    """renvoie les splines sélectionnées et le premier objet polygonal (MNT)
       du document actif"""

    splines = doc.GetActiveObjectsFilter(1,c4d.Ospline,c4d.NOTOK)
    if not splines :
        c4d.gui.MessageDialog(TXT_NO_SPLINE)
        return False

    if not checkSpline(splines):
        rep = c4d.gui.QuestionDialog(TXT_CHECK_SPLINE)
        if not rep : return False

    polyobj = doc.GetActiveObjectsFilter(1,c4d.Opolygon,c4d.NOTOK)
    if not polyobj:
        c4d.gui.MessageDialog(TXT_NO_POLYOBJECT)
        return False

    #si il y a au moins un objet polygonal on prend le premier
    if polyobj : mnt = polyobj[0]

    if len(polyobj)>1:
        rep = c4d.gui.QuestionDialog(TXT_MANY_POLYOBJECT.format(mnt.GetName()))
        if not rep : return False
        
    return splines,mnt

def main():
    res = getSplinesAndMNT()
    if not res : return
    splines,mnt = res
    print(res)




# Execute main()
if __name__=='__main__':
    main()