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
    scale,units = doc[c4d.DOCUMENT_DOCUNIT].GetUnitScale()
    
    print(scale)
    if units==c4d.DOCUMENT_UNIT_KM:
        print('km')
    elif units==c4d.DOCUMENT_UNIT_M:
        print('m')
    elif units==c4d.DOCUMENT_UNIT_CM:
        print('cm')
    elif units==c4d.DOCUMENT_UNIT_MM:
        print('mm')
        
    print(op.GetRad()*2)

# Execute main()
if __name__=='__main__':
    main()