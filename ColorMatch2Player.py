#!/usr/bin/env python

# ColorGame
# Gioco per DUE persone
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

# Pulsanti giocatore A
btnA_R = Button(14) # rosso
btnA_G = Button(15) # verde
btnA_B = Button(18) # blu
# Pulsanti giocatore B
btnB_R = Button(25) # rosso
btnB_G = Button(8) # verde
btnB_B = Button(7) # blu
# Punteggio dei giocatori
pntA = 0
pntB = 0

tempoMax= 5 #timeout

while True:
    # inizializza i flag di uscita
    timeout   = False # tempo non scaduto
    bothresp  = False # non hanno risposto entrambi

    winA = False
    winB = False
    pressA = False
    pressB = False

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

    # definizione della funzione esito
    def esito(resp):
        if int(resp)==risultato:
            return True
        else:
            return False

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
    rispostaA= -2 # indica risposta non data
    rispostaB= -2 # indica risposta non data
    #risposta = raw_input("    risposta: ")

    while (winA or winB) or (pressA and pressB) or (not timeout) or (not bothresp): # ciclo attivo finche' uno indovina o rispondono entrambi o non finisce il tempo:
        time.sleep(0.1)
        tempoTrascorso = time.time() - startTime
        countDown = tempoMax - tempoTrascorso
        #conto = '%03.1f\r' % countDown
        #print conto,
        if btnA_R.is_pressed or btnA_G.is_pressed or btnA_B.is_pressed: # il giocatore A ha risposto
            pressA = True
            # controllo pressione multipla
            if (btnA_R.is_pressed and btnA_G.is_pressed) or (btnA_R.is_pressed and btnA_B.is_pressed) or (btnA_G.is_pressed and btnA_B.is_pressed):
                rispostaA=-1 # ha imbrogliato
            else:
                if   btnA_R.is_pressed:
                    rispostaA=0
                elif btnA_G.is_pressed:
                    rispostaA=1
                elif btnA_B.is_pressed:
                    rispostaA=2
                esitoA = esito(rispostaA)
                if esitoA: # se ha indovinato si deve uscire dal ciclo
                    winA = True
        if btnB_R.is_pressed or btnB_G.is_pressed or btnB_B.is_pressed: # il giocatore A ha risposto
            pressB = True
            # controllo pressione multipla
            if (btnB_R.is_pressed and btnB_G.is_pressed) or (btnB_R.is_pressed and btnB_B.is_pressed) or (btnB_G.is_pressed and btnB_B.is_pressed):
                rispostaB=-1 # ha imbrogliato
            else:
                if btnB_R.is_pressed:
                    rispostaB=0
                elif btnB_G.is_pressed:
                    rispostaB=1
                elif btnB_B.is_pressed:
                    rispostaB=2
                esitoB = esito(rispostaA)
                if esitoB: # se ha indovinato si deve uscire dal ciclo
                    winB = True
        if pressA and pressB: # se entrambi hanno dato una risposta (anche errata)
            bothresp=True
            break
        if tempoTrascorso > tempoMax:
            timeout=True
            break

    if timeout:
        print '    TEMPO SCADUTO!'

    # 7. Calcola l'esito (Ok, No, Tempo scaduto)
    if winA:
        pntA += 1 # incrementa punteggio A
    if winB:
        pntB += 1 # incrementa punteggio B
    textpntA = '%d                  ' % pntA
    textpntB = '%d                  ' % pntB
    textpntAB = textpntA + textpntB

    if winA and winB:
        printcolor('************************************'); print
        printcolor('*  RISPOSTA ESATTA CONTEMPORANEA!  *'); print
        printcolor('************************************'); print
    elif winA:
        printcolor('************************************'); print
        printcolor('*   RISPOSTA ESATTA GIOCATORE A!   *'); print
        printcolor('************************************'); print
    elif winB:
        printcolor('************************************'); print
        printcolor('*   RISPOSTA ESATTA GIOCATORE B!   *'); print
        printcolor('************************************'); print
    elif bothresp and timeout:
        printcolor('************************************'); print
        printcolor('*           TEMPO SCADUTO!         *'); print
        printcolor('*              sveglia!            *'); print
        printcolor('************************************'); print
    else:
        print      '------------------------------------'
        print      '     TUTTE RISPOSTE SBAGLIATE       '
        print      '             merdacce!              '
        print      '------------------------------------'

        print
        printcolor(textpntAB); print


    time.sleep(3)
    print
    print '        Riprovate'
    time.sleep(1)



