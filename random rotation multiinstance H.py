import c4d,math
from random import random
# Welcome to the world of Python


# Script state in the menu or the command palette
# Return True or c4d.CMD_ENABLED to enable, False or 0 to disable
# Alternatively return c4d.CMD_ENABLED|c4d.CMD_VALUE to enable and check/mark
#def state():
#    return True

def randomRotMatriceH():
    angle = random()*math.pi*2
    return c4d.utils.MatrixRotY(angle)

def randomRotMultiInst(multi_inst):
    matrices = [m*randomRotMatriceH() for m in multi_inst.GetInstanceMatrices()]
    multi_inst.SetInstanceMatrices(matrices)
    multi_inst.Message(c4d.MSG_UPDATE)

# Main function
def main():
    multi_inst = op
    randomRotMultiInst(multi_inst)
    c4d.EventAdd()


# Execute main()
if __name__=='__main__':
    main()