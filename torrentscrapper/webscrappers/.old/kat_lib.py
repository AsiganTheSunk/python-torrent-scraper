#!/usr/bin/python

import requests
from bs4 import BeautifulSoup
#from libtorrent.SimpleClientTorrent import st_client
import sys

from main.libtorrent.Magnet2Torrent import m2t_create


def kat_request_constructor (title, season, episode):
    r = (title.replace(" ","%20") +'%20S' +season +'E' +episode +'/')
    return (r)


def kat_usearch(url):
    r = requests.get(url, verify=True)
    return (r)


def kat_parser(content):
    soup = BeautifulSoup(content.text, "html.parser")
    table = soup.findAll('table', {"class": "data"})

    myMagnetList = []
    mySeedList = []
    myLeechList = []
    mySizeList = []
    myNameList = []

    for row in table:
        data_name = row.findAll ('a', {"class":"normalgrey font12px plain bold"})
        for name in data_name:
            myNameList.append(name['href'])
            print ' NAME: ' + name['href'] + 'GB\n'
    
        data_sizes=row.findAll('td', {'class':'nobr center'})
        for sizes in data_sizes:
            aux = sizes.text
            aux_number = aux[:-2]
            aux_metric = aux[-2:]
            if aux_metric == 'GB':
                mySizeList.append(float(aux_number)*1000)
                print ' SIZE: ' + aux_number
            else:
                print "hola" #mySizeList.append(float(aux_number))


        data_seeds=row.findAll('td', {'class':'green center'})
        for seeds in data_seeds:
            mySeedList.append (int (seeds.text))
            print ' SEEDS: ' + seeds.text

        data_leechs=row.findAll('td', {'class':'red lasttd center'})
        for leechs in data_leechs:
            myLeechList.append (int(leechs.text))
            print ' LEECHS: ' + leechs.text + '\n'

        data_magnets=row.findAll ('a', {'title':'Torrent magnet link'})
        for magnet in data_magnets:
            myMagnetList.append (magnet['href'])
            print ' MAGNET: ' +  magnet['href'] + '\n'

        #PANDAS
        #df=DataFrame({'tname':myNameList,'tsize':mySizeList,'tseed':mySeedList,'tleech':myLeechList,'tmagnet':myMagnetList})
        #df['thealth'] = (df['tseed']*100)/(df['tseed']+df['tleech']+0.00000001) # Calculating Torrent Health
        #df = df[df['thealth'] > 50]     #Filter THealth > 50%
        #df = df[df['tsize'] > 500]      #Filter Tam < 600MB
        #df = df.reset_index(drop=True)  #Reset the index to avoid (0,4,7...)
                    
        #for index , rows in df.iterrows():
        #    print ("{0:^30s} {1:^8s} {2:^6s} {3:^6s} {4:^6s}".format(df['tname'][index],'-  SIZE: [ '+color.green(str(df['tsize'][index]) +' MB')+' ]','SEED: [ '+color.red(str(df['tseed'][index]))+' ]', 'LEECH: [ '+color.blue(str(df['tleech'][index]))+' ]','HEALTH:  [ '+ color.cyan(str(df['thealth'][index])[0:2]+'%') +' ]'))

    return
    #return (df)

# def main (search):
#     content = kat_usearch (search)
#     data_frame = kat_parser (content)
#     print "-------------------------------------------------\n"
#
#     try:
#         magnet_number = raw_input ("Selecciona un Numero de Indice de Torrent [0 a N]: ")
#     except KeyboardInterrupt:
#         sys.exit(0)
    
    # magnet = data_frame['tmagnet'][int(magnet_number)]
    # tname = "testCOCO"
    # torrent = m2t_create (magnet, tname)
    # st_client (torrent)
