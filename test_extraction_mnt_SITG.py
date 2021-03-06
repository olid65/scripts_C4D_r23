import c4d
import requests
from pprint import pprint

# Script state in the menu or the command palette
# Return True or c4d.CMD_ENABLED to enable, False or 0 to disable
# Alternatively return c4d.CMD_ENABLED|c4d.CMD_VALUE to enable and check/mark
#def state():
#    return True
NB_PIXELS_MAX = 1024

def dimBbox(xmin,ymin,xmax,ymax):
    largeur = xmax-xmin
    hauteur = ymax-ymin
    return largeur,hauteur

def roundBbox(xmin,ymin,xmax,ymax, nb =0):
    return round(xmin,nb),round(ymin,nb),round(xmax,nb),round(ymax,nb)

def centreBbox(xmin,ymin,xmax,ymax):
    return (xmin+xmax)/2, (ymin+ymax)/2

# Main function
def main():
    # https://ge.ch/sitgags2/rest/services/RASTER/MNA_TERRAIN/ImageServer/exportImage?bbox=2463049.5889072716%2C1086110.9272231692%2C2532057.0889072716%2C1155999.9272231692&bboxSR=2056&size=1024%2C1024&imageSR=&time=&format=tiff&pixelType=F32&noData=&noDataInterpretation=esriNoDataMatchAny&interpolation=+RSP_BilinearInterpolation&compression=&compressionQuality=&bandIds=&mosaicRule=&renderingRule=&f=pjson
    url_base = 'https://ge.ch/sitgags2/rest/services/RASTER/MNA_TERRAIN/ImageServer/exportImage'
    xmin,ymin,xmax,ymax = 2501394.5889073,1113994.9272232,2505009.5889073,1118794.9272232
    centreX,centreY = centreBbox(xmin,ymin,xmax,ymax)
    #xmin,ymin,xmax,ymax = roundBbox(xmin,ymin,xmax,ymax)
    largeur,hauteur = dimBbox(xmin,ymin,xmax,ymax)
    print(largeur,hauteur)
    val_px = max(largeur,hauteur)/NB_PIXELS_MAX
    print (val_px)
    sizeX = round((largeur/val_px))
    sizeY = round((hauteur/val_px))
    
    
    xmin = centreX - sizeX*val_px/2
    xmax = centreX + sizeX*val_px/2
    ymin = centreY - sizeY*val_px/2
    ymax = centreY + sizeY*val_px/2

    print(sizeX,sizeY)
    print(xmin,ymin,xmax,ymax)

    bbox = f"{xmin},{ymin},{xmax},{ymax}"
    params = {  "f" :"json",
                "bbox" : bbox,
                "size":f"{sizeX},{sizeY}",
                "format":"tiff",
                "pixelType":"F32",
                }


    r = requests.get(url_base,params = params)

    if r.status_code == 200:
        print(r.json())
                
    return

    urls_base = ['https://ge.ch/sitgags2/rest/services/CARTES_HISTORIQUES',
                 'https://ge.ch/sitgags2/rest/services/RASTER',
                 ]

    for url_base in urls_base:
        r = requests.get(url_base,params = params)
        print(url_base.split('/')[-1])
        #pprint(dir(r))
        #pprint(r.request.url)
        if r.status_code == 200:
            for service in r.json()['services']:
                name = service['name'].split('/')[-1]
                typ = service['type']
                url = f"{url_base}/{name}/{typ}"

                print('    ',name, typ, url)
        print('-----------------------')




# Execute main()
if __name__=='__main__':
    main()