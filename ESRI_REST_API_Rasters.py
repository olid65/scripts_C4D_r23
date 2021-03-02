import c4d
import requests, json


#On part du principe que le doc est enregistré, géoréférencé,
# pour l'affichage que c'est bien une vue de haut

#vérifier avant que le chemin de l'image n'existe pas etc ....'

FORMATS = { '.jpg':'jpg',
            '.png':'png',
            '.tif':'tiff'}


def extract(url,mini,maxi,px_larg,px_haut,fn_img, calage = False):
    if 'MapServer' in url:
        url += '/export?'
    elif 'ImageServer' in url:
        url += '/exportImage?'

    id_lyr = 0
    bbox = '{0}%2C{1}%2C{2}%2C{3}'.format(mini.x,mini.z,maxi.x,maxi.z) # 2499639.5233%2C1117120.08436258%2C2500839.57718198%2C1118560.1287&
    #size = '{0},{1}'.format(px_larg,px_haut)
    #bboxSR = '2056'
    #imageSR = '2056'
    #"layers":f"show:{id_lyr}"
    params ={"f":"json",
             "bbox":f"{mini.x},{mini.z},{maxi.x},{maxi.z}",
             "size":f"{px_larg},{px_haut}",
             "format": FORMATS[fn_img[-4:]],
             }
    r = requests.get(url,params)
    if r.status_code ==200:
        rjson = r.json()
        url_img = rjson.get('href')
        if url_img:
            r_img = requests.get(url_img)
            if r_img.status_code == 200:
                #écriture du fichier image
                with open(fn_img, 'wb') as f:
                    for chunk in r_img.iter_content(1024):
                        f.write(chunk)
                #ecriture du fichier json
                if calage :
                    fn_json = fn_img[:-3]+'json'
                    with open(fn_json,'w') as fj:
                        json.dump(rjson,fj,indent = 4)
                return True
    return None



# Main function
def main():
    xmin,ymin,xmax,ymax = 2500085.3406755547,1117135.9435388364,2500801.4375391216,1117750.0042827881
    mini = c4d.Vector(xmin,0,ymin)
    maxi = c4d.Vector(xmax,0,ymax)
    fn_img = '/Users/donzeo/Documents/TEMP/SITG_extraction_images/tests/test1.jpg'
    fn_img = '/Users/donzeo/Documents/TEMP/SITG_extraction_images/tests/test1.tif'
    larg,haut = 850,999
    url = 'https://ge.ch/sitgags2/rest/services/RASTER/ORTHOPHOTOS_HISTORIQUES/MapServer'
    url = 'https://ge.ch/sitgags2/rest/services/RASTER/MNA_TERRAIN/ImageServer'
    extract(url,mini,maxi,larg,haut,fn_img)

# Execute main()
if __name__=='__main__':
    main()