import c4d
import requests, json
from pprint import pprint
from datetime import datetime
import subprocess



# Script state in the menu or the command palette
# Return True or c4d.CMD_ENABLED to enable, False or 0 to disable
# Alternatively return c4d.CMD_ENABLED|c4d.CMD_VALUE to enable and check/mark
#def state():
#    return True

class Bbox(object):
    
    def __init__(self,xmin,ymin,xmax,ymax):
         self.xmin,self.ymin,self.xmax,self.ymax = xmin,ymin,xmax,ymax
        
def imageFromRepJson(rjson,fn_img, calage = True):
    """importe le fichier image depuis une requete json
       si calage est sur True écrit également un fichier de calage json selon ESRI rest"""
    url_img = rjson['href']
    ext = url_img[-4:]
    r_img = requests.get(url_img)
    if r_img.status_code == 200:
        with open(fn_img, 'wb') as f:
            for chunk in r_img.iter_content(1024):
                f.write(chunk)
        if calage :
            fn_calage = fn_img[:-3]+'.json'
            with open(fn_calage,'w') as fj:
                json.dump(rjson,fj,indent = 4)

# Main function
def main():
    
    #lecture des infos de base -> (faut-il les stocker avant ??)
    url = 'https://ge.ch/sitgags2/rest/services/RASTER/MNA_TERRAIN/ImageServer'
    
    params = {'f':'json'}
    
    r = requests.get(url, params)
    if r.status_code ==200:
        rjson = r.json()
        
        pxSizeX = rjson.get('pixelSizeX')
        pxSizeY = rjson.get('pixelSizeY')
        pxType = rjson.get('pixelType')
        
        extent = rjson.get('extent')
        if extent:
            xmax = extent.get('xmax')
            xmin = extent.get('xmin')
            ymax = extent.get('ymax')
            ymin = extent.get('ymin')
            
            bbox_server = Bbox(xmin,ymin,xmax,ymax)
            
    
    #calcul de la taille du MNT
    
    xmin,ymin,xmax,ymax = 2499219.995622537,1119707.5333590957,2499783.495622537,1120268.0333590957
    bbox = Bbox(xmin,ymin,xmax,ymax)
    
    nb_px_x = int(round((xmax-xmin)/pxSizeX))
    nb_px_y = int(round((ymax-ymin)/pxSizeY))
    
    #TODO si le MNT est trop grand -> avertir + boîte de dialogue pour changer la taille du pixel ?    
    print(nb_px_x,nb_px_y)
    
    #extraction
    params = { 'f':'json',
               "bbox":f"{xmin},{ymin},{xmax},{ymax}",
               "size":f"{nb_px_x},{nb_px_y}",
               "format": 'tiff',
               "pixelType":'F32',
    }
    
    r = requests.get(url+'/exportImage?', params)
    
    if r.status_code == 200:
        rjson = r.json()
        #pour le format de la date regarder : https://docs.python.org/fr/3/library/datetime.html#strftime-strptime-behavior
        dt = datetime.now()
        time_extract = dt.strftime("%y%m%d_%H%M%S")
        fn_mnt_tif = f'/Users/donzeo/Documents/TEMP/SITG_extraction_images/mna_terrain_{time_extract}.tif' 
        imageFromRepJson(rjson,fn_mnt_tif, calage = False)
        
        fn_mnt_asc = fn_mnt_tif.replace('.tif','.asc')
        proc = subprocess.Popen(['/Applications/QGIS3.10.app/Contents/MacOS/bin/gdal_translate',
                                     '-of','AAIGrid',
                                     fn_mnt_tif,
                                     fn_mnt_asc])

# Execute main()
if __name__=='__main__':
    main()