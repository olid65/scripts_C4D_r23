import c4d
import shapefile
import os


CONTAINER_ORIGIN =1026473

def fichierPRJ(fn):
    fn = os.path.splitext(fn)[0]+'.prj'
    f = open(fn,'w')
    f.write("""PROJCS["CH1903+_LV95",GEOGCS["GCS_CH1903+",DATUM["D_CH1903+",SPHEROID["Bessel_1841",6377397.155,299.1528128]],PRIMEM["Greenwich",0],UNIT["Degree",0.017453292519943295]],PROJECTION["Hotine_Oblique_Mercator_Azimuth_Center"],PARAMETER["latitude_of_center",46.95240555555556],PARAMETER["longitude_of_center",7.439583333333333],PARAMETER["azimuth",90],PARAMETER["scale_factor",1],PARAMETER["false_easting",2600000],PARAMETER["false_northing",1200000],UNIT["Meter",1]]""")
    f.close()


def bbox2shapefile(mini,maxi):
    
    poly = [[[mini.x,mini.z],[mini.x,maxi.z],[maxi.x,maxi.z],[maxi.x,mini.z]]]
    

    #fn = '/Volumes/mip/mandats/02_en_cours/15-EAUX_VIVES/SIG/cadrage_maquette.shp'
    fn = c4d.storage.LoadDialog(flags = c4d.FILESELECT_SAVE)
    
    if not fn : return
    with shapefile.Writer(fn,shapefile.POLYGON) as w:
        w.field('id','I')
        w.record(1)
        w.poly(poly)
        
        fichierPRJ(fn)

    
if __name__=='__main__':
    bbox2shapefile(c4d.Vector(),c4d.Vector(100))
