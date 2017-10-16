#!/usr/bin/env python

# ColorMatch
# Gioco per DUE persone con display a matrice di LED RGB
# Bisogna individuare il colore di una scritta che riporta il nome di un altro colore

# 0. Impostazione librerie
# 1. Impostazione matrici e vettori
#  1.a impostazione parametri per Led matrix
# 2. Estrazione semi
# 3. Calcolo risultato
# 5. Fai partire il timer
# 4. Visualizza marker e disposizione su console
#  4a Idem su RGB matrix
# 6. Attendi la risposta
#  6a aggiorna RGB matrix
# 7. Calcola l'esito e risportalo su console
#  7a Visualizza su RGB matrix

#0. Importazione librerie
import random  # per estrarre a caso i colori e le combinazioni
import time    # per gestire il tempo trascorso
from gpiozero import Button # per gestire i pulsanti dei giocatori
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics # per gestire la matrice led RGB

# 1. Impostazione variabili matrici e vettori
testo = [0, 1, 2] # lista dei testi
nome  = ['   ROSSO   ', '   VERDE   ', '   +BLU+   ']
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
# punteggio da raggiungere
pntMax = 3
# durata del singolo test
tempoMax= 5

# 1.a impostazioni per il ledmatrix
# opzioni
options = RGBMatrixOptions()
options.hardware_mapping = 'adafruit-hat'
options.rows = 32
options.chain_length = 2
# impostazione matrice
matrix = RGBMatrix(options = options)
offline_matrix = matrix.CreateFrameCanvas()
#caricamento font
font1 = graphics.Font()
font2 = graphics.Font()
font3 = graphics.Font()
font4 = graphics.Font()
font1.LoadFont("./fonts/6x10.bdf")  # per nomi dei colori
font2.LoadFont("./fonts/10x20.bdf") # per marker o punteggi
font3.LoadFont("./fonts/4x6.bdf")   # per i tempi
font4.LoadFont("./fonts/9x18.bdf")  # per punteggi
#COLORI GENERICI
RGBColor = [graphics.Color(255, 0, 0), graphics.Color(0, 255, 0), graphics.Color(0, 0, 255)] # colori R-G-B per ledmatrix
#COLORI-TESTI
RGBtxtPos = [[0, 7],[34, 7], [17, 16]                      # posizioni H-V delle scritte dei colori
RGBtxtTxt = [nome[0].strip, nome[1].strip, nome[2].strip]  # nomi dei colori (R-G-B) presi da quelli per la console ma senza gli spazi
# i colori sono legati alle estrazioni dei semi
#MARKER
RGBmrkPos = [27, 31]
RGBmrkLH  = [8, 14]
# il colore e' legato all'estrazione del seme
# funzione per disegnare il marker
def marker(mrkposH, mrkposV, mrkL, mrkH, mrkcol):
    lineEndX = mrkposH + mrkL
    for i in range(mrkH):
        lineY = mrkposV - i
        graphics.DrawLine(offline_matrix, mrkposH, lineY, lineEndX, lineY, mrkcol)
#TIME
RGBtimePos = [[14,27], [39,27]]     # posizioni dei due segnatempo
RGBtimeColNrm  = graphics.Color(180, 180, 180)
RGBtimeColErr  = graphics.Color( 80,  80,  80)
RGBtimeColWin  = graphics.Color(255, 255, 255)
RGBtimeUlPos = [[14,28], [39,28]] # sottolineatura dopo pressione del pulsante
RGBtimeUlLng  = 9
#SCORE
RGBscorePos = [[0,29], [56,29]]     # posizioni dei punteggi
RGBscoreColNrm = graphics.Color(220, 220, 220)
RGBscoreColWin = graphics.Color(255, 255, 255)
#SCELTA (pulsante premuto dal giocatore)
RGBchoicePos = [[0,16], [56,16]]    # posizioni dei marcatori di scelta
RGBchoiceLH  = [7,4]
# il colore e' legato alla scelta del giocatore
def choice(side, color):
    if   side=='Sx':
        marker(RGBchoicePos[0][0], RGBchoicePos[0][1], RGBchoiceLH[0], RGBchoiceLH[1], color)
    elif side=='Dx':
        marker(RGBchoicePos[1][0], RGBchoicePos[1][1], RGBchoiceLH[0], RGBchoiceLH[1], color)
    else:
        print 'errore'

while True: # ciclo della PARTITA. Uscita quando si vince la partita (controlo alla fine)
    # inizializza i flag di uscita di ogni test
    timeout   = False # indica se il tempo e' scaduto
    pressA    = False # indica se A ha risposto. Non si puo' dare piu' di una risposta
    pressB    = False # indica se B ha risposto. Non si puo' dare piu' di una risposta
    bothresp  = False # indica se hanno risposto entrambi
    winA      = False # indica se A ha indovinato
    winB      = False # indica se B ha indovinato
    oneguess  = False # indica se c'e' uno che ha indovinato

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
    # definizione della funzione esito che indice se la scelta fatta e' giusta
    def esito(resp):
        if int(resp)==risultato:
            return True
        else:
            return False

    # 4. Visualizza marker e disposizione

    # CONSOLE
    def printcolor(text, color=7): # funzione per stampare testo a colori sulla console
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
    #Marker
    print
    printcolor('************************************', semeMarker)
    print
    printcolor('************************************', semeMarker)
    print
    print      '------------------------------------'
    #Colori
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
    print      '------------------------------------'
    print
    #printcolor('     0     ')
    #printcolor(            '     1     ')
    #printcolor(                        '     2     ')
    #print
    #print nome[0],nome[1],nome[2]

    # RGB MATRIX
    # impostazione elementi non variabili durante un punto
    # Colori-testi 0-1-2
    RGBnome0 = RGBtxtTxt[elenco[0]]
    RGBnome1 = RGBtxtTxt[elenco[0]]
    RGBnome2 = RGBtxtTxt[elenco[0]]
    RGBcolore0 = RGBColor[colore0]
    RGBcolore1 = RGBColor[colore1]
    RGBcolore2 = RGBColor[colore2]

    # 5. Fai partire il timer
    tempoTrascorso=0
    countDown = tempoMax
    startTime=time.time() # invece di far partire il timer prendo il tempo di inizio

    # 6. Attendi la risposta
    print
    #print countDown,
    rispostaA= -2 # indica risposta non data
    rispostaB= -2 # indica risposta non data
    #risposta = raw_input("    risposta: ")

    while True: # Ciclo del PUNTO. Uscita quando uno indovina o quando rispondono entrambi o quando finisce il tempo (controllo alla fine)
        # pulisce la matrice offline da comporre
        offline_matrix.Clear()

        #aggiornamento tempo
        tempoTrascorso = time.time() - startTime
        countDown = tempoMax - tempoTrascorso
        #conto = '%03.1f\r' % countDown
        #print conto,

        if (not pressA) and (btnA_R.is_pressed or btnA_G.is_pressed or btnA_B.is_pressed): # il giocatore A ha risposto per la prima volta, sono ignorate le altre
            pressA = True # A ha risposto
            # controllo pressione multipla
            if (btnA_R.is_pressed and btnA_G.is_pressed) or (btnA_R.is_pressed and btnA_B.is_pressed) or (btnA_G.is_pressed and btnA_B.is_pressed):
                rispostaA=-1 # ha imbrogliato
                # Choice RGB
                choiceColA    = RGBtimeColErr # marcatore di scelta grigio, scelta non consentita
                RGBtimeColorA = RGBtimeColErr
            else:
                if   btnA_R.is_pressed:
                    rispostaA=0
                elif btnA_G.is_pressed:
                    rispostaA=1
                elif btnA_B.is_pressed:
                    rispostaA=2
                esitoA = esito(rispostaA)
                print 'A ha scelto ' + nome[rispostaA]
                # Choice RGB
                choiceColA = RGBColor[rispostaA])
                if esitoA: # se ha indovinato si deve uscire dal ciclo
                    winA = True
                    oneguess = True
                    RGBtimeColorA = RGBtimeColWin
                    RGBscoreColorA = RGBscoreColWin

        if (not pressB) and (btnB_R.is_pressed or btnB_G.is_pressed or btnB_B.is_pressed): # il giocatore A ha risposto per la prima volta, sono ignorate le altre
            pressB = True
            # controllo pressione multipla
            if (btnB_R.is_pressed and btnB_G.is_pressed) or (btnB_R.is_pressed and btnB_B.is_pressed) or (btnB_G.is_pressed and btnB_B.is_pressed):
                rispostaB=-1 # ha imbrogliato
                # Choice RGB
                choiceColB = RGBtimeColErr # marcatore di scelta grigio, scelta non consentita
            else:
                if btnB_R.is_pressed:
                    rispostaB=0
                elif btnB_G.is_pressed:
                    rispostaB=1
                elif btnB_B.is_pressed:
                    rispostaB=2
                esitoB = esito(rispostaB)
                print 'B ha scelto ' + nome[rispostaB]
                # Choice RGB
                choiceColB = RGBColor[rispostaB])
                if esitoB: # se ha indovinato si deve uscire dal ciclo
                    winB = True
                    oneguess = True
                    RGBtimeColorB = RGBtimeColWin
                    RGBscoreColorB = RGBscoreColWin
        # aggiornamento tempi dei due giocatori
        if not pressA:
            RGBtimeStrA = str(countDown) # aggiorna il tempo A se non ha premuto pulsanti
        if not pressB:
            RGBtimeStrB = str(countDown) # aggiorna il tempo B se non ha premuto pulsanti

        # RGB MATRIX
        # disegno elementi non variabili durante un punto
        # Colori-Nomi
        graphics.DrawText(offline_matrix, font1, RGBtxtPos[0][0], RGBtxtPos[0][1], RGBcolore0, RGBnome0)
        graphics.DrawText(offline_matrix, font1, RGBtxtPos[1][0], RGBtxtPos[1][1], RGBcolore1, RGBnome1)
        graphics.DrawText(offline_matrix, font1, RGBtxtPos[2][0], RGBtxtPos[2][1], RGBcolore2, RGBnome2)
        #Marker
        marker(RGBmrkPos[0], RGBmrkPos[1], RGBmrkLH[0], RGBmrkLH[1], RGBColor[semeColore])
        # disegno elementi variabili durante un punto
        #Time Sx e Dx
        graphics.DrawText(offline_matrix, font3, RGBtimePos[0][0], RGBtimePos[0][1], RGBtimeColorA, RGBtimeStrA)
        graphics.DrawText(offline_matrix, font3, RGBtimePos[1][0], RGBtimePos[1][1], RGBtimeColorB, RGBtimeStrA)
        #sottolineatura tempo
        if pressA:
            graphics.DrawLine(offline_matrix, RGBtimeUlPos[0][0], RGBtimeUlPos[0][1], RGBtimeUlPos[0][0]+RGBtimeUlLng, RGBtimeUlPos[0][1], RGBtimeColorA)
        if pressB:
            graphics.DrawLine(offline_matrix, RGBtimeUlPos[0][0], RGBtimeUlPos[1][1], RGBtimeUlPos[1][0]+RGBtimeUlLng, RGBtimeUlPos[1][1], RGBtimeColorB)
        #Score Sx e Dx
        graphics.DrawText(offline_matrix, font4, RGBscorePos[0][0], RGBscorePos[0][1], RGBscoreColNrm, str(pntA))
        graphics.DrawText(offline_matrix, font4, RGBscorePos[1][0], RGBscorePos[1][1], RGBscoreColNrm, str(pntB))
        #Choice Sx e Dx
        choice('Sx', choiceColA)
        choice('Dx', choiceColB)

        # aggiornamento immagine sul display
        offline_matrix = matrix.SwapOnVSync(offline_matrix)

        # attesa, da tarare
        time.sleep(0.05) # spostare alla fine

        # condizioni di uscita
        if oneguess:          # se uno ha indovinato
            break
        if pressA and pressB: # se entrambi hanno dato una risposta errata
            bothresp=True
            break
        if tempoTrascorso > tempoMax: # se il tempo e' scaduto
            timeout=True
            break

    # 7. Calcola l'esito
    if winA:
        pntA += 1 # incrementa punteggio A
    if winB:
        pntB += 1 # incrementa punteggio B
    textpntA = '%d                 ' % pntA
    textpntB = '                 %d' % pntB
    textpntAB = textpntA + textpntB

    # possibili esiti:
    # 1. risposta giusta contemporanea di entrambi
    if winA and winB:
        printcolor('************************************'); print
        printcolor('*  RISPOSTA ESATTA CONTEMPORANEA!  *'); print
        printcolor('************************************'); print
    # 2. risposta giusta di A
    elif winA:
        printcolor('************************************'); print
        printcolor('*   RISPOSTA ESATTA GIOCATORE A!   *'); print
        printcolor('************************************'); print
    # 3. risposta giusta di B
    elif winB:
        printcolor('************************************'); print
        printcolor('*   RISPOSTA ESATTA GIOCATORE B!   *'); print
        printcolor('************************************'); print
    # 4. nessuno ha risposto giusto
    else:
        # nessuno ha risposto
        if ((not pressA) and (not pressB)):
            printcolor('************************************'); print
            printcolor('*           TEMPO SCADUTO!         *'); print
            printcolor('*              sveglia!            *'); print
            printcolor('************************************'); print
        # ha risposto solo A, sbagliando
        elif pressA and not pressB:
            print      '------------------------------------'
            print      '       A: RISPOSTA SBAGLIATA        '
            print      '       B: TEMPO SCADUTO             '
            print      '------------------------------------'
        # ha risposto solo B, sbagliando
        elif pressB and not pressA:
            print      '------------------------------------'
            print      '       A: TEMPO SCADUTO             '
            print      '       B: RISPOSTA SBAGLIATA        '
            print      '------------------------------------'
        # hanno risposto entrambi sbagliando
        else:
            print      '------------------------------------'
            print      '     TUTTE RISPOSTE SBAGLIATE       '
            print      '             merdacce!              '
            print      '------------------------------------'

    # stampa i punteggi
    print
    printcolor(textpntAB); print

    if pntA==pntMax or pntB==pntMax:
        time.sleep(0.5)
        print
        print     '         PARTITA TERMINATA'
        if pntA==pntMax:
            print '        VINCE IL GIOCATORE A '
        else:
            print '        VINCE IL GIOCATORE B '
        time.sleep(3)
        break
    else:
        time.sleep(3)
        print
        print     '             Pronti....'
        time.sleep(1)



