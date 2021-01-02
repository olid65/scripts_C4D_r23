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
    #lecture du dossier source
    url_source = 'https://ge.ch/sitgags2/rest/services/RASTER'
    params = {  "f" :"json",
    }

    r = requests.get(url_source,params = params)
    #pprint(dir(r))
    #pprint(r.request.url)
    if r.status_code == 200:
        for service in r.json()['services']:
            name = service['name'].split('/')[-1]
            typ = service['type']
            url = f"{url_source}/{name}/{typ}"

            if typ == 'MapServer':

                r2 = requests.get(url,params = params)

                if r2.status_code == 200:
                    
                    if len(r2.json()['layers'])>1:
                        print (name,len(r2.json()['layers']))
                        for lyr in r2.json()['layers']:
                            print('    ',lyr['name'])
                        print('--------')




# Execute main()
if __name__=='__main__':
    main()