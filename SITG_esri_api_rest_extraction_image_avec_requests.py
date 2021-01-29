import c4d
import requests
from pprint import pprint


# Script state in the menu or the command palette
# Return True or c4d.CMD_ENABLED to enable, False or 0 to disable
# Alternatively return c4d.CMD_ENABLED|c4d.CMD_VALUE to enable and check/mark
#def state():
#    return True

# Main function
def main():
    url = 'https://ge.ch/sitgags2/rest/services/RASTER/ORTHOPHOTOS_2019/MapServer/export?'
    bbox = '2496860.357319213,1113079.0650721174,2503603.327606115,1122552.0218986375'
    params = {"f":"json",
              "bbox":bbox,
              "size":"1024,1024",
              "format":"jpg"}
              
    fn_img = '/Users/donzeo/Documents/TEMP/SITG_raster/test.jpg'
    
    r = requests.get(url, params = params)
    
    if r.status_code ==200:
        rjson = r.json()
        extent = rjson['extent']
        
        url_img = rjson['href']
        ext = url_img[-4:]
        print(url_img)
        r_img = requests.get(url_img)
        
        if r_img.status_code == 200:
            with open(fn_img, 'wb') as f:
                for chunk in r_img.iter_content(1024):
                    f.write(chunk)
        
        #pprint(r.json())
    

# Execute main()
if __name__=='__main__':
    main()