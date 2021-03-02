# coding: utf-8

import c4d

url = "http://ge.ch/sitg/sitg_catalog/data_details/66f600c4-4745-4842-99d1-b52e8ae17e21/xhtml"

class DialogHTML(c4d.gui.GeDialog):
    """ classe pour afficher rapidement une page HTML
        __init__(url, nom =None)
        nom [optionnel] = titre de la bo^îte de dialogue
        lancer avec dlg.Open(c4d.DLG_TYPE_ASYNC)"""

    def __init__(self,url, name = None):
        if name == None:
            name = url
        self.name = name
        self.url_base = url
        c4d.gui.GeDialog.__init__(self)
        #self.AddGadget(c4d.DIALOG_NOMENUBAR, 0)

    # In the dialog class define this function
    def HtmlViewerCallback(self, user_data, url, encoding) :
        self.url = url

    def CreateLayout(self):
        self.SetTitle(self.name)
        self.b = self.AddCustomGui(1000, c4d.CUSTOMGUI_HTMLVIEWER, "",
            c4d.BFH_SCALEFIT | c4d.BFV_SCALEFIT, 200, 200)
        self.b.SetURLCallback(self.HtmlViewerCallback)
        return True

    def InitValues(self):
        self.b.SetUrl(self.url_base, c4d.URL_ENCODING_UTF16)
        self.b.SetURLCallback(self.HtmlViewerCallback)
        return True
    
if __name__=='__main__':
    dlg = DialogHTML(url)
    dlg.Open(c4d.DLG_TYPE_ASYNC)