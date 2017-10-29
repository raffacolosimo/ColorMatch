#! /usr/bin/python
'''
Script per lanciare un altro script e lanciarlo di nuovo se questo termina per un errore
'''
# Imposta dei valori di default
# ripeti:
#   prova a lanciare lo script
#

import subprocess
COUNTER=0
while True: # ciclo infinito di lancio dello script
    COUNTER=COUNTER+1
    print "*** LANCIO ColorMatch *** Esecuzione n.%d" % (COUNTER)
    try:
        subprocess.call(["sudo", "python", "/home/pi/Documents/ColorMatch/ColorMatch2Player-RGB.py"])
    except:
        print "Errore"

