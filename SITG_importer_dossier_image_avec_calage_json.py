import c4d, json, os
from glob import glob
from pprint import pprint

CONTAINER_ORIGIN =1026473

def creer_mat(fn,nom,alpha=False):
        mat = c4d.BaseMaterial(c4d.Mmaterial)
        mat.SetName(nom)
        doc.InsertMaterial(mat)
        shd = c4d.BaseList2D(c4d.Xbitmap)
        shd[c4d.BITMAPSHADER_FILENAME] = fn
        mat[c4d.MATERIAL_COLOR_SHADER] = shd
        mat.InsertShader(shd)
        mat[c4d.MATERIAL_USE_SPECULAR]=False
    
        if alpha :
            mat[c4d.MATERIAL_USE_ALPHA]=True
            shda = c4d.BaseList2D(c4d.Xbitmap)
            shda[c4d.BITMAPSHADER_FILENAME] = fn 
            mat[c4d.MATERIAL_ALPHA_SHADER]=shda
            mat.InsertShader(shda)
            
        mat.Message(c4d.MSG_UPDATE)
        mat.Update(True, True)
        return mat 


# Main function
def main():
    
    ext = '.json'
    path = f'/Users/donzeo/SWITCHdrive/PYTHON/Requests_ESRI_REST_API/cartes/*{ext}'
    res = c4d.BaseObject(c4d.Onull)
    res.SetName('CARTES')
    origin = doc[CONTAINER_ORIGIN]
    
    for fn in sorted(glob(path)):
        with open(fn) as f:
            
            name = os.path.basename(fn)[:-len(ext)]
            
            fn_img = fn.replace(ext,'.png')
            mat = creer_mat(fn_img,name)
            doc.InsertMaterial(mat)
            
            data = json.load(f)
            xmax = data['extent']['xmax']
            xmin = data['extent']['xmin']
            ymax = data['extent']['ymax']
            ymin = data['extent']['ymin']
            
            
            centre = c4d.Vector((xmax+xmin)/2,0,(ymin+ymax)/2)
            
            if not origin :
                doc[CONTAINER_ORIGIN] = centre
                origin = centre
                
            larg = xmax-xmin
            haut = ymax-ymin
            
            plan = c4d.BaseObject(c4d.Oplane)
            plan[c4d.PRIM_PLANE_WIDTH] = larg
            plan[c4d.PRIM_PLANE_HEIGHT] = haut

            plan[c4d.PRIM_PLANE_SUBW] = 0
            plan[c4d.PRIM_PLANE_SUBH] = 0
            
            plan.SetAbsPos(centre -origin)
            
            plan.SetName(name)
            plan.InsertUnderLast(res)
            
            tag = c4d.TextureTag()
            tag.SetMaterial(mat)
            tag[c4d.TEXTURETAG_PROJECTION]= c4d.TEXTURETAG_PROJECTION_UVW
            plan.InsertTag(tag)
            
    doc.InsertObject(res) 
    c4d.EventAdd()       

# Execute main()
if __name__=='__main__':
    main()