# -*- coding: utf-8 -*-
# Functions to process images

import os

def generateEmail(requestFolder, name, url):
	path = os.join(requestFolder, 'static/emails/postcard.html')
	email = open(path, 'r').readlines()
	print email.split('<head>')[0]
	

