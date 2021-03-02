import c4d,os
import json
from pprint import pprint

CONTAINER_ORIGIN =1026473

O_DEFAUT = c4d.Vector(2500000.00,0.0,1120000.00)
# Script state in the menu or the command palette
# Return True or c4d.CMD_ENABLED to enable, False or 0 to disable
# Alternatively return c4d.CMD_ENABLED|c4d.CMD_VALUE to enable and check/mark
#def state():
#    return True

# Main function
def main():
    fn = '/Users/donzeo/SWITCHdrive/PYTHON/Requests_ESRI_REST_API/CARTE_NATIONALE_25K_1956_2009.json'
    fn = '/Users/donzeo/SWITCHdrive/PYTHON/Requests_ESRI_REST_API/CARTES_DUFOUR_1845_1935.json'
    fn = '/Users/donzeo/SWITCHdrive/PYTHON/Requests_ESRI_REST_API/PLAN_BASE_ARCHIVE_1936_2002.json'
    
    res = c4d.BaseObject(c4d.Onull)
    res.SetName(os.path.basename(fn))
    origin = doc[CONTAINER_ORIGIN]
    if not origin:
        doc[CONTAINER_ORIGIN] = O_DEFAUT
        origin = O_DEFAUT

    with open(fn) as f:
        data = json.load(f)
        url = data['url']
        for feat in data['features']:
            attr = feat['attributes']
            geom = feat['geometry']['rings'][0]
            pts = [c4d.Vector(x,0,y)-origin for x,y in geom]
            name = attr['Name']

            sp = c4d.SplineObject(len(pts), c4d.SPLINETYPE_LINEAR)
            sp.SetName(name)
            sp.SetAllPoints(pts)
            sp.Message(c4d.MSG_UPDATE)
            sp.InsertUnderLast(res)

    doc.InsertObject(res)
    c4d.EventAdd()



# Execute main()
if __name__=='__main__':
    main()