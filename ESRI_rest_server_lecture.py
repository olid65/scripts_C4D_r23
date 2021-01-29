import c4d
import os.path
import requests
from pprint import pprint


# Script state in the menu or the command palette
# Return True or c4d.CMD_ENABLED to enable, False or 0 to disable
# Alternatively return c4d.CMD_ENABLED|c4d.CMD_VALUE to enable and check/mark
#def state():
#    return True

# Main function
def main():
    dir_name = os.path.dirname(__file__)
    fn_srces = 'ESRI_rest_server.txt'
    params = {  "f" :"json",
    }
    
    with open(os.path.join(dir_name,fn_srces)) as f:
        for server in f.read().split():
            pos = server.find('//')
            print(server[pos+2:])
            
            continue
            print('')
            r = requests.get(server,params = params)
            if r.status_code == 200:
                for service in r.json()['services']:
                    #
                    name = service['name'].split('/')[-1]
                    typ = service['type']
                    url = f"{server}/{name}/{typ}"
                    print(url)
                    
            print('---------')
            
    
    return
    #lecture du dossier source
    url_source = 'https://ge.ch/sitgags2/rest/services'
    params = {  "f" :"json",
    }

    r = requests.get(url_source,params = params)
    #pprint(dir(r))
    #pprint(r.request.url)
    if r.status_code == 200:
        pprint(r.json())
        pass

# Execute main()
if __name__=='__main__':
    main()