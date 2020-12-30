import c4d



# Script state in the menu or the command palette
# Return True or c4d.CMD_ENABLED to enable, False or 0 to disable
# Alternatively return c4d.CMD_ENABLED|c4d.CMD_VALUE to enable and check/mark
#def state():
#    return True


class DlgBbox(c4d.gui.GeDialog):
    
    N_MIN = 1015
    N_MAX = 1016
    E_MIN = 1017
    E_MAX = 1018
    
    BTON_FROM_OBJECT = 1050
    BTON_FROM_VIEW = 1051
    BTON_COPY_ALL = 1052
    BTON_N_MIN = 1055
    BTON_N_MAX = 1056
    BTON_E_MIN = 1057
    BTON_E_MAX = 1058
    
    
    MARGIN = 5
    LARG_COORD = 250

    def CreateLayout(self):
        
        self.SetTitle("Emprise géographique")
        #CADRAGE
        self.GroupBegin(500,flags=c4d.BFH_CENTER, cols=3, rows=1)
        self.GroupBorderSpace(self.MARGIN, self.MARGIN, self.MARGIN, self.MARGIN)  
        self.AddStaticText(1001,name="N max :", flags=c4d.BFH_MASK,initw=50)
        self.AddEditNumber(self.N_MAX, flags=c4d.BFH_MASK, initw=self.LARG_COORD, inith=0)
        self.AddButton(self.BTON_N_MAX,flags=c4d.BFH_MASK, initw=0, inith =0, name ="copier")
        self.GroupEnd()
        
        self.GroupBegin(500,flags=c4d.BFH_CENTER, cols=7, rows=1)
        self.GroupBorderSpace(self.MARGIN, self.MARGIN, self.MARGIN, self.MARGIN)  
        self.AddStaticText(1003,name="E min :", flags=c4d.BFH_MASK,initw=50)
        self.AddEditNumber(self.E_MIN, flags=c4d.BFH_MASK, initw=self.LARG_COORD, inith=0)
        self.AddButton(self.BTON_E_MIN,flags=c4d.BFH_MASK, initw=0, inith =0, name ="copier")
        self.AddStaticText(1005,name="", flags=c4d.BFH_MASK,initw=200)
        self.AddStaticText(1004,name="E max :", flags=c4d.BFH_MASK,initw=50)
        self.AddEditNumber(self.E_MAX, flags=c4d.BFH_MASK, initw=self.LARG_COORD, inith=0)
        self.AddButton(self.BTON_E_MAX,flags=c4d.BFH_MASK, initw=0, inith =0, name ="copier")
        self.GroupEnd()
        
        self.GroupBegin(500,flags=c4d.BFH_CENTER, cols=3, rows=1)
        self.GroupBorderSpace(self.MARGIN, self.MARGIN, self.MARGIN, self.MARGIN) 
        self.AddStaticText(1002,name="N min :", flags=c4d.BFH_MASK,initw=50)
        self.AddEditNumber(self.N_MIN, flags=c4d.BFH_MASK, initw=self.LARG_COORD, inith=0)
        self.AddButton(self.BTON_N_MIN,flags=c4d.BFH_MASK, initw=0, inith =0, name ="copier")
        self.GroupEnd()
        
        self.GroupBegin(500,flags=c4d.BFH_LEFT, cols=1, rows=1)
        self.GroupBorderSpace(self.MARGIN, self.MARGIN, self.MARGIN, self.MARGIN) 
        
        self.AddStaticText(1004,name="REMARQUE", flags=c4d.BFH_MASK)
        
        self.GroupEnd()
        
        self.GroupBegin(500,flags=c4d.BFH_CENTER, cols=3, rows=1)
        self.GroupBorderSpace(self.MARGIN, self.MARGIN, self.MARGIN, self.MARGIN) 
        
        self.AddButton(self.BTON_FROM_OBJECT,flags=c4d.BFH_MASK, initw=150, inith =0, name ="depuis la sélection")
        self.AddButton(self.BTON_FROM_VIEW,flags=c4d.BFH_MASK, initw=150, inith =0, name ="depuis la vue")
        self.AddButton(self.BTON_COPY_ALL,flags=c4d.BFH_MASK, initw=150, inith =0, name ="copier toutes les valeurs")
        
        self.GroupEnd()

        return True
    
    def InitValues(self):
        self.SetMeter(self.N_MAX, 0.0)
        self.SetMeter(self.N_MIN, 0.0)
        self.SetMeter(self.E_MIN, 0.0)
        self.SetMeter(self.E_MAX, 0.0)
        return True
    
    def Command(self,id,msg):

        if id == self.BTON_FROM_OBJECT:
            print('BTON_FROM_OBJECT')
        if id == self.BTON_FROM_VIEW:
            print('BTON_FROM_VIEW')
        if id == self.BTON_COPY_ALL:
             print('BTON_COPY_ALL')
        if id == self.BTON_N_MIN :
             print('BTON_N_MIN')
        if id == self.BTON_N_MAX:
            print('BTON_N_MAX')
        if id == self.BTON_E_MIN:
            print('BTON_E_MIN')
        if id == self.BTON_E_MAX:
            print('BTON_E_MAX')
            
        return True

# Execute main()
if __name__=='__main__':
    dlg = DlgBbox()
    dlg.Open(c4d.DLG_TYPE_ASYNC)