import c4d
import requests
from pprint import pprint
from datetime import datetime
import time


# Script state in the menu or the command palette
# Return True or c4d.CMD_ENABLED to enable, False or 0 to disable
# Alternatively return c4d.CMD_ENABLED|c4d.CMD_VALUE to enable and check/mark
#def state():
#    return True


URL_BASE = 'https://ge.ch/sitgags2/rest/services/CARTES_HISTORIQUES'

class MyThread(c4d.threading.C4DThread) :

    def Main(self) :
        url_base =  URL_BASE
        params = {"f":"json"}
        r = requests.get(url_base,params = params)
        if r.status_code == 200:
            rjson = r.json()
            for service in rjson['services']:
                name = service['name'].split('/')[-1]
                #if name =='CARTES_DUFOUR_1845_1935':
                typ = service['type']
                url = f"{url_base}/{name}/{typ}"
                r2 = requests.get(url,params = params)
                if r2.status_code == 200:
                    if 'Catalog' in r2.json()['capabilities']:
                        r3 = requests.get(url+'/query?', params)
                        print(r3.url)
                        if r3.status_code == 200:
                            
                            features = r3.json().get('features',None)
                            if features :
                                print(name)
                                for feature in features:
                                    print(feature['attributes']['OBJECTID'])
                                
                            print('------------------------------------------------------------')


def readRacine(url_base):
    pass


# Execute main()
if __name__=='__main__':
    thread = MyThread()
    thread.Start()