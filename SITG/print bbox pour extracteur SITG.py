import c4d
from c4d import gui
CONTAINER_ORIGIN =1026473


def main():
    o = doc[CONTAINER_ORIGIN]
    pos = op.GetMg().off
    mp = op.GetMp()
    rad = op.GetRad()
    
    centre = o+pos+mp
    
    c4d.CopyStringToClipboard(str(centre.x-rad.x))
    print ('min.x :')
    print (str(centre.x-rad.x))
    print ('min.y :')
    print (str(centre.z-rad.z))
    print ('max.x :')
    print (str(centre.x+rad.x))
    print ('max.y :')
    print (str(centre.z+rad.z))

if __name__=='__main__':
    main()
