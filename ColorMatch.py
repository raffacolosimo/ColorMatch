#!/usr/bin/env python

# ColorGame
# Gioco per una persona
# Bisogna individuare il colore di una scritta che riporta il nome di un altro colore

# 1. Impostazione matrici e vettori
# 2. Estrazione semi
# 3. Calcolo risultato
# 4. Visualizza marker e disposizione
#  4a Idem su RGB matrix
# 5. Fai partire il timer
# 6. Attendi la risposta
#  6a aggiorna RGB matrix
# 7. Calcola l'esito (Ok, No, Tempo scaduto)
#  7a Visualizza su RGB matrix

import random
import time
from gpiozero import Button

# 1. Impostazione variabili matrici e vettori
testo = [0, 1, 2] # lista dei testi
nome  = [' ROSSO ', ' VERDE ', ' +BLU+ ']
var = [0,1] # lista variazioni del colore della scritta
disp = [0,1,2,3,4,5] # lista della disposizione da visualizzare
#                 0        1        2
testoEColore = [[1,2],   [2,0],   [0,1]] # lista di liste, 3x2
#                 0         1        2        3        4        5
disposizione = [[0,1,2], [0,2,1], [1,2,0], [1,0,2], [2,0,1], [2,1,0]] # lista di liste, 6x3

button_r = Button(14) # rosso
button_g = Button(15) # verde
button_b = Button(18) # blu

tempoMax= 5 #timeout

while True:
    # 2. Estrazione semi
    semeMarker = random.choice(testo)
    semeColore = random.choice(var)
    semeDisposizione = random.choice(disp)
    
    #print 'SemeMarker: ' + str(semeMarker)
    #print 'SemeColore: ' + str(semeColore)
    #print 'SemeDisposizione: ' + str(semeDisposizione)
    
    # 3. Calcolo risultato
    risultato = testoEColore [semeMarker][semeColore]
    #print
    #print 'Risultato: ' + str(risultato)
    
    # 4. Visualizza marker e disposizione
    def printcolor(text, color=7):
        if color==0:
            colorindex = 1
        if color==1:
            colorindex = 2
        if color==2:
            colorindex = 4
        if color==7:
            colorindex = 7
        colorstring  ='\033[1;3%dm%s\033[1;m' % (colorindex, text)
        print colorstring,
    
    print
    printcolor('**********************', semeMarker)
    print
    print '----------------------'
    elenco = disposizione[semeDisposizione]
    nome0 = nome[elenco[0]]
    nome1 = nome[elenco[1]]
    nome2 = nome[elenco[2]]
    colore0 = testoEColore[elenco[0]][semeColore]
    colore1 = testoEColore[elenco[1]][semeColore]
    colore2 = testoEColore[elenco[2]][semeColore]
    printcolor(nome0, colore0)
    printcolor(nome1, colore1)
    printcolor(nome2, colore2)
    print
    print '----------------------'
    print
    printcolor('   0   ')
    printcolor('   1   ')
    printcolor('   2   ')
    print
    print nome[0],nome[1],nome[2]
    
    # 5. Fai partire il timer
    startTime=time.time() # invece di far partire il timer prendo il tempo di inizio
    tempoTrascorso=0
    countDown = tempoMax
    # 6. Attendi la risposta
    print
    #print countDown,
    risposta=-2
    #risposta = raw_input("    risposta: ")
    while True:
        time.sleep(0.1)
        tempoTrascorso = time.time() - startTime
        countDown = tempoMax - tempoTrascorso
        #conto = '%03.1f\r' % countDown
        #print conto,  
        
        if button_r.is_pressed or button_g.is_pressed or button_b.is_pressed or tempoTrascorso > tempoMax:
            if button_r.is_pressed:
                risposta=0
            elif button_g.is_pressed:
                risposta=1
            elif button_b.is_pressed:
                risposta=2
            else:
                risposta=-1
            break
	if risposta>=0: 
		print '   Hai scelto ' + nome[risposta] 
    if (risposta == -1):
		print '    TEMPO SCADUTO!'
    
    # 7. Calcola l'esito (Ok, No, Tempo scaduto)
    if int(risposta)==risultato:
        printcolor('**********************'); print
        printcolor('*  RISPOSTA ESATTA!  *'); print
        printcolor('**********************'); print
    elif int(risposta)>=0:
        print '----------------------'
        print '  RISPOSTA SBAGLIATA'
        print '      merdaccia!'
        print '----------------------'
    
    time.sleep(3)
    print
    print '        Riprova'
    time.sleep(1)



