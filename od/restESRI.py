#!/usr/bin/python
# -*- coding: utf-8 -*-

import c4d, urllib,json,os
from od import emprises

class Service(object):

	def __init__(self, url, typ, bboxImg, format = 'jpg'):
		self.url = url
		self.bboxImg = bboxImg
		self.type = typ
		self.format = format

	def urlRequest(self):

		if self.type == 'ImageServer':
			service = '/exportImage?'
		else:
			service = '/export?'

		return "{0}{1}bbox={2}&size={3}&format={4}&f=pjson".format(self.url,service,self.bboxImg.bboxREST,self.bboxImg.sizeREST,self.format)





def main():
    pass    

if __name__=='__main__':
    main()
