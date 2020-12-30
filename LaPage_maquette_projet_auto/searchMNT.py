import c4d

MNT_NAME = 'MNT'.lower()

def searchMNT(start, res = None):
    """renvoie le premier objet dont le nom contient MNT_NAME (insensible à la casse)"""
    while start:
        name = start.GetName().lower()
        if MNT_NAME in name and start.GetType()==c4d.Opolygon:
            res =  start
        if res : return res
        res = searchMNT(start.GetDown(),res)
        if res : return res
        start = start.GetNext()
    return res 

# Main function
def main():
    print(searchMNT(doc.GetFirstObject()))

# Execute main()
if __name__=='__main__':
    main()