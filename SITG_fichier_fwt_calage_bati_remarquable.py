import c4d,os
from glob import glob

OA_OFFSET_FILE_NAME = 'Offset_OA.txt'

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

def read_OA_Offset(fn):
    with open(fn) as f :
        transx = float(f.readline().split()[-1])
        transz = float(f.readline().split()[-1])
        return c4d.Vector(transx,0,transz)



# Main function
def main():

    path = '/Users/donzeo/Documents/Mandats/SITG/format_z_3D_3DS_OUVRAGES_canton_all_20210113_134339'
    path = '/Users/donzeo/Documents/Mandats/SITG/format_z_3D_3DS_OUVRAGES_canton_all_20210113_134339/12_quai_du_Rhone'
    path = '/Users/donzeo/Documents/Mandats/SITG'
    #recuperation de tous les fichier 3ds
    for fn_3ds in getFilesFromDir_recursive(path,ext ='.3ds'):
        dir_up,name = os.path.split(fn_3ds)
        print(name)
        
        fn_offset = os.path.join(dir_up,OA_OFFSET_FILE_NAME)
        
        #fichier calage pour les bati remarquables
        fn_fwt = fn_3ds.replace('.3ds','.fwt')
        if os.path.isfile(fn_fwt):
            print(readFWT(fn_fwt))

        #sinon on regarde si on a un fichier Offset_OA.txt pour les ouvrages d'art'
        elif os.path.isfile(fn_offset) :
            print(fn_offset)
            print(read_OA_Offset(fn_offset))



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