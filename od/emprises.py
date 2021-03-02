#!/usr/bin/python
# -*- coding: utf-8 -*-

import c4d, math, random
from od.od_const import CONTAINER_ORIGIN

class Bbox(object):
    def __init__(self,mini,maxi):

        self.min = mini
        self.max = maxi
        self.centre = (self.min+self.max)/2
        self.largeur = self.max.x - self.min.x
        self.hauteur = self.max.z - self.min.z
        self.taille = self.max-self.min

    def intersect(self,bbx2):
        """video explicative sur http://www.youtube.com/watch?v=8b_reDI7iPM"""
        return ( (self.min.x+ self.taille.x)>= bbx2.min.x and
                self.min.x <= (bbx2.min.x + bbx2.taille.x) and
                (self.min.z + self.taille.z) >= bbx2.min.z and
                self.min.z <= (bbx2.min.z + bbx2.taille.z))
        
    def xInside(self,x):
        """retourne vrai si la variable x est entre xmin et xmax"""
        return x>= self.min.x and x<= self.max.x
    
    def zInside(self,y):
        """retourne vrai si la variable x est entre xmin et xmax"""
        return y>= self.min.z and y<= self.max.z
        
    def isInsideX(self,bbox2):
        """renvoie 1 si la bbox est complètement à l'intérier
           renoive 2 si elle est à cheval
           et 0 si à l'extérieur"""
        minInside = self.xInside(bbox2.xmin)
        maxInside = self.xInside(bbox2.xmax)
        if minInside and maxInside : return 1
        if minInside or maxInside : return 2
        #si bbox1 est plus grand
        if bbox2.xmin < self.min.x and bbox2.xmax > self.max.x : return 2
        return 0
    
    def isInsideZ(self,bbox2):
        """renvoie 1 si la bbox est complètement à l'intérier
           renoive 2 si elle est à cheval
           et 0 si à l'extérieur"""
        minInside = self.zInside(bbox2.ymin)
        maxInside = self.zInside(bbox2.ymax)
        if minInside and maxInside : return 1
        if minInside or maxInside : return 2
        #si bbox1 est plus grand
        if bbox2.ymin < self.min.z and bbox2.ymax > self.max.z : return 2
        return 0
    
    def ptIsInside(self,pt):
        """renvoie vrai si point c4d est à l'intérieur"""
        return  self.xInside(pt.x) and self.zInside(pt.z)

    def getRandomPointInside(self, y = 0):
        x = self.min.x + random.random()*self.largeur
        z = self.min.z + random.random()*self.hauteur
        return c4d.Vector(x,y,z)
    
    def GetSpline(self,origine = c4d.Vector(0)):
        """renvoie une spline c4d de la bbox"""
        res = c4d.SplineObject(4,c4d.SPLINETYPE_LINEAR)
        res[c4d.SPLINEOBJECT_CLOSED] = True
        res.SetAllPoints([c4d.Vector(self.min.x,0,self.max.z)-origine,
                           c4d.Vector(self.max.x,0,self.max.z)-origine,
                           c4d.Vector(self.max.x,0,self.min.z)-origine,
                           c4d.Vector(self.min.x,0,self.min.z)-origine])
        res.Message(c4d.MSG_UPDATE)
        return res
    def __str__(self):
        return ('X : '+str(self.min.x)+'-'+str(self.max.x)+'->'+str(self.max.x-self.min.x)+'\n'+
                'Y : '+str(self.min.z)+'-'+str(self.max.z)+'->'+str(self.max.z-self.min.z))

    def GetCube(self,haut = 200):
    	res = c4d.BaseObject(c4d.Ocube)
    	taille = c4d.Vector(self.largeur,haut,self.hauteur)
    	res.SetAbsPos(self.centre)
    	return res
    
    @staticmethod
    def fromObj(obj,origine = c4d.Vector()):
        """renvoie la bbox 2d de l'objet"""
        mg = obj.GetMg()
    
        rad = obj.GetRad()
        centre = obj.GetMp()
        
        #4 points de la bbox selon orientation de l'objet
        pts = [ c4d.Vector(centre.x+rad.x,centre.y+rad.y,centre.z+rad.z) * mg,
                c4d.Vector(centre.x-rad.x,centre.y+rad.y,centre.z+rad.z) * mg,
                c4d.Vector(centre.x-rad.x,centre.y-rad.y,centre.z+rad.z) * mg,
                c4d.Vector(centre.x-rad.x,centre.y-rad.y,centre.z-rad.z) * mg,
                c4d.Vector(centre.x+rad.x,centre.y-rad.y,centre.z-rad.z) * mg,
                c4d.Vector(centre.x+rad.x,centre.y+rad.y,centre.z-rad.z) * mg,
                c4d.Vector(centre.x-rad.x,centre.y+rad.y,centre.z-rad.z) * mg,
                c4d.Vector(centre.x+rad.x,centre.y-rad.y,centre.z+rad.z) * mg]
    
        mini = c4d.Vector(min([p.x for p in pts]),min([p.y for p in pts]),min([p.z for p in pts])) + origine
        maxi = c4d.Vector(max([p.x for p in pts]),max([p.y for p in pts]),max([p.z for p in pts])) + origine
    
        return Bbox(mini,maxi)
    
    @staticmethod
    def fromView(basedraw,origine = c4d.Vector()):
        dimension = basedraw.GetFrame()
        largeur = dimension["cr"]-dimension["cl"]
        hauteur = dimension["cb"]-dimension["ct"]
    
        mini =  basedraw.SW(c4d.Vector(0,hauteur,0)) + origine
        maxi = basedraw.SW(c4d.Vector(largeur,0,0)) + origine
        return Bbox(mini,maxi)

class BboxImg(Bbox):
    """Même chose que la classe mère Bbox mais avec des attributs de nombre de pixels en x et en y"""
    
    def __init__(self,mini,maxi,px_x,px_y):
        super(BboxImg,self).__init__(mini,maxi)
        self.px_x = px_x
        self.px_y = px_y
        self.taille_px = c4d.Vector(self.largeur/px_x,self.hauteur/px_y,0)
    @property
    def sizeREST(self):
        return '{0}%2C{1}'.format(self.px_x,self.px_y)
    @property
    def bboxREST(self):
        return '{0}%2C{1}%2C{2}%2C{3}'.format(self.min.x,self.min.z,self.max.x,self.max.z)  

    @staticmethod
    def fromView(basedraw,origine = c4d.Vector()):
        dimension = basedraw.GetFrameScreen()
        largeur = dimension["cr"]-dimension["cl"]
        hauteur = dimension["cb"]-dimension["ct"]
    
        mini =  basedraw.SW(c4d.Vector(0,hauteur,0)) + origine
        maxi = basedraw.SW(c4d.Vector(largeur,0,0)) + origine
        return BboxImg(mini,maxi, largeur,hauteur)    

    @staticmethod
    def fromObj(obj,resolution,origine = c4d.Vector()):
        bbx = super(BboxImg,BboxImg).fromObj(obj,origine)
        largeur = int(bbx.largeur / resolution)
        hauteur = int(bbx.hauteur / resolution)
        return BboxImg(bbx.min,bbx.max,largeur,hauteur)
          
    def __str__(self):
        return super(BboxImg,self).__str__() + '\npixels x : {0}\npixels y : {1}'.format(self.px_x,self.px_y)
    
class Tuiles(object):
    
    def __init__(self,bbox,taille_du_px,nb_px_max=4096, regulier = False):
        """ si regulier est sur True les tuiles ont toutes la même taille
            sinon on étend la bbox pour avoir toutes des mailles carées
            coresspondantes à la taille max"""
        
        self.bbox = bbox
        self.taille_max = taille_du_px * nb_px_max

        #calcul du nombre en largeur et hauteur
        self.nb_larg = int(math.ceil(bbox.largeur/(taille_du_px*nb_px_max)))
        self.nb_haut = int(math.ceil(bbox.hauteur/(taille_du_px*nb_px_max)))
        
        if regulier:
            l = self.nb_larg * nb_px_max * taille_du_px
            h = self.nb_haut * nb_px_max * taille_du_px
            v = c4d.Vector(l/2.,0,h/2.)
            mini = bbox.centre - v
            maxi = bbox.centre + v
            self.bbox = Bbox(mini,maxi)
            

        self.bboxes = []    
        
        #GRILLE

        taille = c4d.Vector(self.bbox.largeur/self.nb_larg,0,self.bbox.hauteur/self.nb_haut)
        nb_px_x = int(round(taille.x/taille_du_px))
        nb_px_y = int(round(taille.z/taille_du_px))
            
        mini = c4d.Vector(self.bbox.min.x,self.bbox.min.y,self.bbox.min.z)
        maxi = mini + taille
        

        
        for i in xrange(self.nb_haut):
            for n in xrange(self.nb_larg):
                bb = BboxImg(c4d.Vector(mini.x,mini.y,mini.z),c4d.Vector(maxi.x,maxi.y,maxi.z),nb_px_x,nb_px_y)
                self.bboxes.append(bb)
                mini.x+= taille.x
                maxi.x+= taille.x
            mini.x = self.bbox.min.x
            maxi.x = mini.x+taille.x
            
            mini.z+= taille.z
            maxi.z+= taille.z
                    
            
    
    def getSplines(self,origine):
        res = c4d.BaseObject(c4d.Onull)
        for bb in self.bboxes: 
            sp = bb.GetSpline(origine)
            sp.InsertUnder(res)
            mg = c4d.Matrix()
            mg.off = bb.centre-origine
            
        return res
        

def main():

    origine = doc[CONTAINER_ORIGIN]
    print (BboxImg.fromObj(op,0.2,origine))
    return
    bd = doc.GetActiveBaseDraw()
    bbx = BboxImg.fromView(bd, origine)
    
    tuiles = Tuiles(bbx,0.05,4096,False)
    doc.InsertObject(tuiles.getSplines(origine))
    c4d.EventAdd()

if __name__=='__main__':
    main()
