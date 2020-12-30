import c4d,csv
from c4d import gui
# Welcome to the world of Python


# Script state in the menu or the command palette
# Return True or c4d.CMD_ENABLED to enable, False or 0 to disable
# Alternatively return c4d.CMD_ENABLED|c4d.CMD_VALUE to enable and check/mark
#def state():
#    return True


def readCSV(fn_csv):
    """renvoie un dictionnaire à partir du fichier csv
       Attention depuis excel choisir CSV (Macintosh) (séparateur :points virgule)(.csv)
       Le csv contient 3 colonnes sans nom :  NOM_FICHIER;NOM_CHAMP;TYPE_CHAMP"""
       
    res = {}
    with open(fn_csv) as file:
        spamreader = csv.reader(file, delimiter=';')
        for filename,fieldname,fieldtype in spamreader:
            res.setdefault(filename,[]).append(fieldname)
    return res

# Main function
def main():
    fn_csv = '/Users/olivier.donze/Mandats/Modele_donnee_LaPage/pay_nivA_listes_table_champ_domain_mdd_v1.0c.csv'
    dic = readCSV(fn_csv)
    for k,lst in dic.items():
        print(k)
        for field in lst:
            print('     ',field)
    


# Execute main()
if __name__=='__main__':
    main()