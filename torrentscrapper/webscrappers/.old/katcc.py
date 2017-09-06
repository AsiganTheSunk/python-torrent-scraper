#!/usr/bin/python
#-*- coding. utf-8 -*-

# Dependencias
# apt-get install python-bs4

import getopt
import sys

import main.webparser.kat_lib
from bs4 import BeautifulSoup
from main.utils import Color

#-----------------------------
title=" "
season=" "
episode=" "

usearch = 'https://kat.cr/usearch/'

def usage():
	print "kat -t title  -s season -c capitule"
	print "-t  title   	Titulo de la Serie"
	print "-s  season  	Temporada de la serie"
	print "-e  episode  	Capitulo de la serie"

def escribe (s):
	print s

try:
# argumentos 1: ht:s:c orden en que pilla los opts
	opts, args = getopt.getopt (sys.argv[1:], "ht:s:e:", ["help","title=","season=","episode="])
except getopt.GetoptError:
	usage()
	sys.exit(2)

for o, a in opts:
	if o in ("-h","--help"):
		usage()
		sys.exit()
	if o in ("-t", "--title"):
		title=a
	if o in ("-s", "--season"):
		season=a
	if o in ("-e", "--episode"):
		episode=a

if(title == " "):
	usage()

#TODO:
#Hace falta incorporar parametro para peliculas

def main ():	
	escribe ('SERIE: [ '+title+' S'+season+' '+' E'+episode+' ]')
	test =  (usearch+title.replace(" ","%20")+'%20S'+season+'E'+episode+'/')
	
	content = main.webparser.kat_lib.kat_usearch (test)
	soup = BeautifulSoup (content.text)
	#r = requests.get (test, verify=False)
	#print r.status_code
	#soup = BeautifulSoup (r.text)
	#print (soup.prettify())

	# TABLE:
	# -- Recuperar la tabla de torrents de kat.cr

	table = soup.find ('table', {"class":"data"}) 
	#print table
	rows = table.find_all ('tr') 
	#print rows
	
	myMagnetList = []
	mySeedList = []
	myLeechList = []
	mySizeList = []
	myTNameList = []
	myNameList = []		

	for row in rows:
		data_name = row.findAll ('a', {'class':'cellMainLink'})
		for name in data_name:
			print name.text
			myNameList.append(name.text)
		data_tnames = row.findAll ('a', {'class':'cellMainLink'})
		for names in data_tnames:
			print names['href']
			myTNameList.append (names['href'])
		data_sizes = row.findAll ('td', {'class':'nobr center'})
		for sizes in data_sizes:
			print sizes.text
			mySizeList.append (str (sizes.text))
		data_seeds =  row.findAll ('td', {'class':'green center'})
		for seeds in data_seeds:
			print seeds.text
			mySeedList.append (int (seeds.text))
		data_leechs = row.findAll ('td', {'class':'red lasttd center'})
		for leechs in data_leechs:
			print leechs.text
			myLeechList.append (int (leechs.text))
		data_magnets = row.findAll ('a',{'class':'imagnet icon16'})
		for magnet in data_magnets:
			print magnet['href']
			myMagnetList.append (magnet['href'])

	struct = zip (myNameList, mySizeList, mySeedList, myLeechList, myMagnetList)

	for name, size, seed, leech, magnet in struct:
		#float(size[:-3]) <--- METRICA
		print ("{0:^30s} {1:^8s} {2:^6s} {3:^6s} {4:^6s}".format(name,'-  SIZE: [ ' + Color.green(size) + ' ]', 'SEED: [ ' + Color.red(str(seed)) + ' ]', 'LEECH: [ ' + Color.blue(str(leech)) + ' ]', 'ACTIVITY:  [ ' + Color.cyan(str(seed + leech)) + ' **]'))

if  __name__ == '__main__':
	if (len(sys.argv) <=1):
		sys.exit(-1)
	else:
		main()
