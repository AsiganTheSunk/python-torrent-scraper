#!/usr/bin/python
#-*- coding. utf-8 -*-

import requests
from bs4 import BeautifulSoup

from main.utils import Color

#Nos conectamos a un proxy de thepiratebay dado que la conexion directa no funciona, no se porque
url_inicio = "https://pirateproxy.tf/s/?q="
url_princ = "https://pirateproxy.tf"

def search(name, temp, ep):
	if ep.replace(' ','') == '':
		url = url_inicio + name.replace(' ','+') + '+' + 'temporada' + '+' + temp
	else:
		url = url_inicio + name.replace(' ','+') + '+' + temp + 'x' + ep
	content = requests.get(url)
	return content

def get_magnet(url):
	content = requests.get(url)
	soup = BeautifulSoup(content.text, "html.parser")
	magnet = soup.find('div',{'class':'download'}).contents[1]['href']
	return magnet

def parse(content):
	soup = BeautifulSoup(content.text, "html.parser")
	rows = soup.findAll('tr')
	rows = rows[1:]
	print content.url
	name_list = []
	size_list = []
	seeds_list = []
	leechs_list = []
	magnets_list = []

	for row in rows:
		name_list.append(row.find('a', {"class":"detLink"}).text)
		size_list.append(" ".join(rows[0].find('font',{'class':'detDesc'}).text.split(',')[1].split()[1:3]))
		seeds_list.append(rows[0].findAll('td',{'align':'right'})[0].text)
		leechs_list.append(rows[0].findAll('td',{'align':'right'})[1].text)

		url = url_princ + row.find('a',{'class':'detLink'})['href']
		magnets_list.append(get_magnet(url))
		#falta ir a esa url a sacar el magnet, get_magnet(url)
	
	struct = zip(name_list, size_list, seeds_list, leechs_list, magnets_list)

	for name, size, seed, leech, magnet in struct:
		#float(size[:-3]) <--- METRICA
		print ("{0:^30s} {1:^8s} {2:^6s} {3:^6s} {4:^6s}".format(name,'-  SIZE: [ ' + Color.green(size) + ' ]', 'SEED: [ ' + Color.red(str(seed)) + ' ]', 'LEECH: [ ' + Color.blue(str(leech)) + ' ]', 'ACTIVITY:  [ ' + Color.cyan(str(seed + leech)) + ' **]'))



def main(name, temp, ep):
	content = search(name, temp, ep)
	parse(content)




