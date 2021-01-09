import c4d
import struct

#https://www.adobe.io/content/dam/udp/en/open/standards/tiff/TIFF6.pdf -> pour le tif
#https://www.usna.edu/Users/oceano/pguth/md_help/html/tbme9v52.htm -> pour le geoTitt


# Main function
def main():
    fn = '/Users/donzeo/Documents/TEMP/test.tif'
    fn = '/Users/donzeo/Downloads/exportImage.tif'
    
    with open(fn,'rb') as f:
        #le premier byte sert à savoir si on es en bigendian ou pas
        r = f.read(2)
        big = True
        if r == b'II':
            big = False
        if big : big ='>'
        else : big = '<'
        #ensuite on a un nombre de verification ? -> normalement 42  sinon 43 pour les bigTiff
        #le second c'est le début du premier IFD (image file directory) en bytes -> 8 en général (commence à 0)
        s = struct.Struct(f"{big}Hl")
        rec = f.read(6)
        print(s.unpack(rec))
        
        #début de l'IFD' normalement commence à 8
        #nombre de tags
        s = struct.Struct(f"{big}H")
        rec = f.read(2)
        nb_tag, = s.unpack(rec)
        print('----')
        
        for i in range(nb_tag):
            s = struct.Struct(f"{big}HHlHH")
            rec = f.read(12)
            print(s.unpack(rec))
        print('----')
        
        #4 bytes pour si on a plusieurs IFD
        s = struct.Struct(f"{big}l")
        rec = f.read(4)
        print(s.unpack(rec))
        
        

# Execute main()
if __name__=='__main__':
    main()