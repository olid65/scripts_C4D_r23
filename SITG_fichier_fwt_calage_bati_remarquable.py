import c4d,os
from glob import glob


# Script state in the menu or the command palette
# Return True or c4d.CMD_ENABLED to enable, False or 0 to disable
# Alternatively return c4d.CMD_ENABLED|c4d.CMD_VALUE to enable and check/mark
#def state():
#    return True

def readFWT(fn):
    """lecture du fichier fwt des b^âtiments remarquables
       cela semble être une matrice 4x4
       il ne semble pas avoir de rotation, mais juste une mise à l'échelle
       donc je n'ai pas tenu compte des rotations éventuelles

       renvoie les vecteurs de translation d'échelle"""
    try :
        with open(fn) as f:
            fwt = f.read().split()
            scalex = float(fwt[0])/100
            transx = float(fwt[3])
            scalez = float(fwt[5])/100
            transz = float(fwt[7])
            scaley = float(fwt[10])/100
            transy = float(fwt[11])

            scale = c4d.Vector(scalex,scaley,scalez)
            translation = c4d.Vector(transx,transy,transz)
    except : return False

    return translation,scale

def getFilesFromDir(pth,ext =''):
    return glob(os.path.join(pth,'*'+ext))

def getFilesFromDir_recursive(pth,ext =''):
    res = []
    if os.path.isdir(pth): res.extend(getFilesFromDir(pth,ext)) 
       
    for pth2 in glob(os.path.join(pth,'*')):
        if os.path.isdir(pth2):
            res.extend(getFilesFromDir_recursive(pth2,ext))
    return res   



# Main function
def main():
    
    path = '/Users/olivier.donze/Downloads/format_z_3D_3DS_OUVRAGES_bat_20210113_091959'
    
    #recuperation de tous les fichier 3ds
    for fn_3ds in getFilesFromDir_recursive(path,ext ='.3ds'):
        print(fn_3ds)
        #fichier calage pour les bati remarquables
        fn_fwt = fn_3ds.replace('.3ds','.fwt')
        if os.path.isfile(fn_fwt):
            print(readFWT(fn_fwt))
            
        #sinon on regarde si on a un fichier Offset_OA.txt pour les ouvrages d'art'
        
        elif :
            
            
        
        print('---')

    return
    fn = '/Users/olivier.donze/Downloads/format_z_3D_3DS_OUVRAGES_bat_20210113_091959/Gare_Cornavin/Gare_Cornavin.fwt'
    with open(fn) as f:
        fwt = f.read().split()
        scalex = float(fwt[0])/100
        transx = float(fwt[3])
        scalez = float(fwt[5])/100
        transz = float(fwt[7])
        scaley = float(fwt[10])/100
        transy = float(fwt[11])

        scale = c4d.Vector(scalex,scaley,scalez)
        translation = c4d.Vector(transx,transy,transz)
        print(scale)
        print(translation)

# Execute main()
if __name__=='__main__':
    main()