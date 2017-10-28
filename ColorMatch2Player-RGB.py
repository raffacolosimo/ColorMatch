#!/usr/bin/env python

# ColorMatch
# Gioco per DUE persone con display a matrice di LED RGB
# Bisogna individuare il colore di una scritta che riporta il nome di un altro colore

# 0. Impostazione librerie
# 1. Impostazione matrici e vettori
#   1.a impostazione parametri e funzioni per Led matrix
#   1.b Animazione iniziale. COLOR MATCH - Premi per un tasto per iniziare
#   1.c Schermata di partenza: Pronti? 3-2-1
# 2. Estrazione semi
# 3. Calcolo risultato
# 4. Visualizza marker e disposizione su console
# 5. Fai partire il timer
# 6. Attendi la risposta
#   6a Schermata RGB matrix durante il punto (tempo che scorre, risposte)
# 7. Calcola l'esito e risportalo su console
#   7a Schermata esito su RGB matrix: Vince A-B, Pari!, A: risposta errata B: tempo scaduto (o viceversa), TEMPO SCADUTO!
# 8 Se la partita non e' finita torna al punto 0.b


print 'inizio'
import pygame.mixer
print 'importato mixer'
pygame.mixer.init()

sound1 = pygame.mixer.Sound("/home/pi/Documents/ColorMatch/sounds/baby_x.wav")
sound2 = pygame.mixer.Sound("/home/pi/Documents/ColorMatch/sounds/buzzer.wav")
print 'suoni caricati'
sound1.play()
print 'riproduzione suono1 '


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
# punteggio da raggiungere
pntMax = 3
# durata del singolo test
tempoMax= 5
# flag di pressione pulsante
pressA = False # indica se ha risposto. Non si puo' dare piu' di una risposta
pressB = False
winA = False
winB = False

# esito e risultato
risultato = '' # varia per ogni punto
# definizione della funzione esito che indice se la scelta fatta e' giusta
def esito(resp):
    if int(resp)==risultato:
        sound1.play()
        return True
    else:
        sound2.play()
        return False

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
font2.LoadFont("./fonts/5x7.bdf")   # per messaggio di esito
font3.LoadFont("./fonts/4x6.bdf")   # per i tempi
font4.LoadFont("./fonts/9x18.bdf")  # per punteggi
#COLORI GENERICI
RGBColor = [graphics.Color(255, 0, 0), graphics.Color(0, 255, 0), graphics.Color(0, 0, 255)] # colori R-G-B per ledmatrix
RGBColBlack = graphics.Color(0, 0, 0)
RGBColWhite = graphics.Color(255, 255, 255)
# per schermata intro
RGB_Rosso = graphics.Color(255,   0,   0)
RGB_Giallo= graphics.Color(255, 255,   0)
RGB_Verde = graphics.Color(  0, 255,   0)
RGB_Viola = graphics.Color(  0, 255, 255)
RGB_Blu   = graphics.Color(  0,   0, 255)

#COLORI-TESTI
RGBtxtPos = [[0, 7],[34, 7], [17, 16]]                      # posizioni H-V delle scritte dei colori
RGBtxtTxt = [nome[0].strip(), nome[1].strip(), nome[2].strip()]  # nomi dei colori presi da quelli per la console ma senza gli spazi
# i colori sono legati alle estrazioni dei semi
RGBcolore0 = RGBColor[0] # solo per inizializzare il tipo
RGBcolore1 = RGBColor[1]
RGBcolore2 = RGBColor[2]
RGBnome0 = RGBtxtTxt[0]  # solo per inizializzare
RGBnome1 = RGBtxtTxt[1]
RGBnome2 = RGBtxtTxt[2]
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
RGBtimePos = [[13,27], [39,27]]     # posizioni dei due segnatempo
RGBtimeColNrm  = graphics.Color( 96,  96,  96)
RGBtimeColErr  = graphics.Color( 48,  48,  48)
RGBtimeColWin  = graphics.Color( 96,  96,  96)
RGBtimeColorA = RGBtimeColNrm # il colore e' legato all'esito
RGBtimeColorB = RGBtimeColNrm
RGBtimeStrA = str(tempoMax)
RGBtimeStrB = str(tempoMax)
#SCORE
RGBscorePos = [[-1,29], [56,29]]     # posizioni dei punteggi
RGBscoreColNrm = graphics.Color(128, 128, 128)
RGBscoreColWin = graphics.Color(255, 255, 255)
RGBscoreColorA = RGBscoreColNrm
RGBscoreColorB = RGBscoreColNrm
#SCELTA (pulsante premuto dal giocatore)
RGBchoicePos = [[13,20], [39,20]]    # posizioni dei marcatori di scelta
RGBchoiceLH  = [10,3]
choiceColA = '' # il colore e' legato alla scelta del giocatore
choiceColB = ''
#RGBchoiceLinePos = [[24,19], [36,19]] # linea dopo pressione del pulsante
#RGBchoiceLineLng  = 2
def choice(side, color):
    if   side=='Sx':
        marker(RGBchoicePos[0][0], RGBchoicePos[0][1], RGBchoiceLH[0], RGBchoiceLH[1], color)
        marker(RGBchoicePos[0][0], RGBchoicePos[0][1]+10, RGBchoiceLH[0], RGBchoiceLH[1], color)
    elif side=='Dx':
        marker(RGBchoicePos[1][0], RGBchoicePos[1][1], RGBchoiceLH[0], RGBchoiceLH[1], color)
        marker(RGBchoicePos[1][0], RGBchoicePos[1][1]+10, RGBchoiceLH[0], RGBchoiceLH[1], color)
    else:
        print 'errore in choice'
def setRGBpart1():
    # RGB MATRIX
    # disegno elementi non variabili durante un punto
    # Colori-Nomi
    graphics.DrawText(offline_matrix, font1, RGBtxtPos[0][0], RGBtxtPos[0][1], RGBcolore0, RGBnome0)
    graphics.DrawText(offline_matrix, font1, RGBtxtPos[1][0], RGBtxtPos[1][1], RGBcolore1, RGBnome1)
    graphics.DrawText(offline_matrix, font1, RGBtxtPos[2][0], RGBtxtPos[2][1], RGBcolore2, RGBnome2)
    #Marker
    marker(RGBmrkPos[0], RGBmrkPos[1], RGBmrkLH[0], RGBmrkLH[1], RGBColor[semeMarker])
def setRGBpart2():
    # disegno elementi variabili durante un punto
    #Time Sx e Dx
    graphics.DrawText(offline_matrix, font3, RGBtimePos[0][0], RGBtimePos[0][1], RGBtimeColorA, RGBtimeStrA)
    graphics.DrawText(offline_matrix, font3, RGBtimePos[1][0], RGBtimePos[1][1], RGBtimeColorB, RGBtimeStrB)
    #sottolineatura tempo e marcatura di scelta
    if pressA:
        #graphics.DrawLine(offline_matrix, RGBchoiceLinePos[0][0], RGBchoiceLinePos[0][1], RGBchoiceLinePos[0][0]+RGBchoiceLineLng, RGBchoiceLinePos[0][1], choiceColA)
        #Choice Sx
        choice('Sx', choiceColA)
    if pressB:
        #graphics.DrawLine(offline_matrix, RGBchoiceLinePos[1][0], RGBchoiceLinePos[1][1], RGBchoiceLinePos[1][0]+RGBchoiceLineLng, RGBchoiceLinePos[1][1], choiceColB)
        #Choice Dx
        choice('Dx', choiceColB)
    #Score Sx e Dx
    graphics.DrawText(offline_matrix, font4, RGBscorePos[0][0], RGBscorePos[0][1], RGBscoreColorA, str(pntA))
    graphics.DrawText(offline_matrix, font4, RGBscorePos[1][0], RGBscorePos[1][1], RGBscoreColorB, str(pntB))
def RGBesitoPnt():
    # cancella la parte superiore del display
    marker(0,16,64,17, RGBColBlack)
    # inserisce un marker con la risposta esatta
    marker(27,22,8,7, RGBColor[risultato])
    graphics.DrawLine(offline_matrix, 31, 29, 31, 23, RGBColor[risultato])
    graphics.DrawLine(offline_matrix, 31, 23, 33, 25, RGBColor[risultato])
    graphics.DrawLine(offline_matrix, 31, 23, 29, 25, RGBColor[risultato])

    # 1. risposta giusta contemporanea di entrambi
    if winA and winB:
        RGBesitoTxt = 'PARI!'
        RGBesitoPosH = 32 - int(5*len(RGBesitoTxt)/2)
        graphics.DrawText(offline_matrix, font2, RGBesitoPosH, 11, RGBtimeColWin, RGBesitoTxt)
    # 2. risposta giusta di A
    elif winA:
        RGBesitoTxt = 'PUNTO PER A'
        RGBesitoPosH = 32 - int(5*len(RGBesitoTxt)/2)
        graphics.DrawText(offline_matrix, font2, RGBesitoPosH, 11, RGBtimeColWin, RGBesitoTxt)
    # 3. risposta giusta di B
    elif winB:
        RGBesitoTxt = 'PUNTO PER B'
        RGBesitoPosH = 32 - int(5*len(RGBesitoTxt)/2)
        graphics.DrawText(offline_matrix, font2, RGBesitoPosH, 11, RGBtimeColWin, RGBesitoTxt)
    # 4. nessuno ha risposto giusto
    else:
        # nessuno ha risposto
        if ((not pressA) and (not pressB)):
            RGBesitoTxt1 = 'TEMPO SCADUTO'
            RGBesitoPosH1 = 32 - int(4*len(RGBesitoTxt1)/2)
            graphics.DrawText(offline_matrix, font3, RGBesitoPosH1, 11, RGBtimeColNrm, RGBesitoTxt1)
        # ha risposto solo A, sbagliando
        elif pressA and not pressB:
            RGBesitoTxt1 = 'A: Errore'
            RGBesitoPosH1 = 32 - int(4*len(RGBesitoTxt1)/2)
            graphics.DrawText(offline_matrix, font3, RGBesitoPosH1, 7, RGBtimeColNrm, RGBesitoTxt1)
            RGBesitoTxt2 = 'B: Fuori tempo'
            RGBesitoPosH2 = 32 - int(4*len(RGBesitoTxt2)/2)
            graphics.DrawText(offline_matrix, font3, RGBesitoPosH2, 13, RGBtimeColNrm, RGBesitoTxt2)
        # ha risposto solo B, sbagliando
        elif pressB and not pressA:
            RGBesitoTxt1 = 'A: Fuori tempo'
            RGBesitoPosH1 = 32 - int(4*len(RGBesitoTxt1)/2)
            graphics.DrawText(offline_matrix, font3, RGBesitoPosH1, 7, RGBtimeColNrm, RGBesitoTxt1)
            RGBesitoTxt2 = 'B: Errore'
            RGBesitoPosH2 = 32 - int(4*len(RGBesitoTxt2)/2)
            graphics.DrawText(offline_matrix, font3, RGBesitoPosH2, 13, RGBtimeColNrm, RGBesitoTxt2)
        # hanno risposto entrambi sbagliando
        else:
            RGBesitoTxt1 = 'TUTTO SBAGLIATO'
            RGBesitoPosH1 = 32 - int(4*len(RGBesitoTxt1)/2)
            graphics.DrawText(offline_matrix, font3, RGBesitoPosH1, 11, RGBtimeColNrm, RGBesitoTxt1)
def CSLesitoPnt():
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
            time.sleep(1)
        # ha risposto solo A, sbagliando
        elif pressA and not pressB:
            print      '------------------------------------'
            print      '       A: RISPOSTA SBAGLIATA        '
            print      '       B: TEMPO SCADUTO             '
            print      '------------------------------------'
            time.sleep(1)
        # ha risposto solo B, sbagliando
        elif pressB and not pressA:
            print      '------------------------------------'
            print      '       A: TEMPO SCADUTO             '
            print      '       B: RISPOSTA SBAGLIATA        '
            print      '------------------------------------'
            time.sleep(1)
        # hanno risposto entrambi sbagliando
        else:
            print      '------------------------------------'
            print      '     TUTTE RISPOSTE SBAGLIATE       '
            print      '             merdacce!              '
            print      '------------------------------------'
            time.sleep(1)
    # stampa i punteggi
    textpntA = '%d                 ' % pntA
    textpntB = '                 %d' % pntB
    textpntAB = textpntA + textpntB
    print
    printcolor(textpntAB); print
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

#   1.b Animazione iniziale. COLOR MATCH
def RGBIntroScreen():
    offline_matrix.Clear() # pulisce la matrice offline da comporre
    COLORfont = font4
    sizeH = 9
    let3X=int(16-sizeH/2)
    let2X=let3 - sizeH
    let4X=let3 + sizeH
    let1X=let2 - sizeH
    let5X=let4 + sizeH
    COLORX = [let1X,let2X,let3X,let4X,let5X]
    COLORY = [15,15,15,15,15]
    COLcolor [RGB_Rosso,RGB_Giallo,RGB_Verde,RGB_Viola,RGB_Blu]

    MATCHX  = [let1X,let2X,let3X,let4X,let5X]
    MATCHY  = [32,32,32,32,32]
    MATcolor= [RGB_Rosso,RGB_Giallo,RGB_Verde,RGB_Viola,RGB_Blu]

    # scritta COLOR
    graphics.DrawText(offline_matrix, COLORfont, COLORX[0], COLORY[0], COLcolor[0], 'C')
    graphics.DrawText(offline_matrix, COLORfont, COLORX[1], COLORY[1], COLcolor[1], 'O')
    graphics.DrawText(offline_matrix, COLORfont, COLORX[2], COLORY[2], COLcolor[2], 'L')
    graphics.DrawText(offline_matrix, COLORfont, COLORX[3], COLORY[3], COLcolor[3], 'O')
    graphics.DrawText(offline_matrix, COLORfont, COLORX[4], COLORY[4], COLcolor[4], 'R')

    # scritta MATCH
    graphics.DrawText(offline_matrix, COLORfont, MATCHX[0], MATCHY[0], MATcolor[0], 'M')
    graphics.DrawText(offline_matrix, COLORfont, MATCHX[1], MATCHY[1], MATcolor[1], 'A')
    graphics.DrawText(offline_matrix, COLORfont, MATCHX[2], MATCHY[2], MATcolor[2], 'T')
    graphics.DrawText(offline_matrix, COLORfont, MATCHX[3], MATCHY[3], MATcolor[3], 'C')
    graphics.DrawText(offline_matrix, COLORfont, MATCHX[4], MATCHY[4], MATcolor[4], 'H')

    offline_matrix = matrix.SwapOnVSync(offline_matrix) # aggiorna il display

#  Premi per un tasto per iniziare
def RGBPressToStart():


#   1.c Schermata di partenza: Pronti? 3-2-1
def RGBReadySetGo():





while True: # ciclo delle partite. Non si esce mai

    RGBIntroScreen()
    time.sleep(2)

    # Punteggio dei giocatori
    pntA = 0
    pntB = 0

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
        semeMarker = random.choice(testo) # sceglie un indice di colore (0-1-2 che punta al relativo testo)
        semeColore = random.choice(var)   # sceglie una variazione (0 o 1)
        semeDisposizione = random.choice(disp) # sceglie una disposizione delle scritte (da 0 a 5)

        # 3. Calcolo risultato
        risultato = testoEColore [semeMarker][semeColore]

        # 4. Visualizza marker e disposizione

        # CONSOLE

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

        # RGB MATRIX

        # impostazione elementi non variabili durante un punto
        # Colori-testi 0-1-2
        RGBnome0 = RGBtxtTxt[elenco[0]] # corrisponde a nome ma senza spazi
        RGBnome1 = RGBtxtTxt[elenco[1]]
        RGBnome2 = RGBtxtTxt[elenco[2]]
        RGBcolore0 = RGBColor[colore0]
        RGBcolore1 = RGBColor[colore1]
        RGBcolore2 = RGBColor[colore2]
        # elementi variabili, ma con valore iniziale certo
        RGBtimeColorA = RGBtimeColNrm
        RGBtimeColorB = RGBtimeColNrm
        RGBscoreColorA = RGBscoreColNrm
        RGBscoreColorB = RGBscoreColNrm
        # 5. Fai partire il timer
        tempoTrascorso=0
        countDown = tempoMax
        startTime=time.time() # invece di far partire il timer prendo il tempo di inizio

        # 6. Attendi la risposta
        rispostaA= -2 # indica risposta non data
        rispostaB= -2 # indica risposta non data

        while True: # Ciclo del PUNTO. Uscita quando uno indovina o quando rispondono entrambi o quando finisce il tempo (controllo alla fine)

            #aggiornamento tempo
            tempoTrascorso = time.time() - startTime
            countDown = tempoMax - tempoTrascorso
            #conto = '%03.1f\r' % countDown
            #print conto,

            if (not pressA) and (btnA_R.is_pressed or btnA_G.is_pressed or btnA_B.is_pressed): # il giocatore A ha risposto per la prima volta, sono ignorate le altre
                pressA = True # A ha risposto
                # aggiorna per l'ultima volta il suo timer
                RGBtimeStrA = '%03.1f' % countDown
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
                    choiceColA = RGBColor[rispostaA]
                    if esitoA: # se ha indovinato si deve uscire dal ciclo
                        winA = True
                        oneguess = True
                        RGBtimeColorA = RGBtimeColWin
                        RGBscoreColorA = RGBscoreColWin

            if (not pressB) and (btnB_R.is_pressed or btnB_G.is_pressed or btnB_B.is_pressed): # il giocatore A ha risposto per la prima volta, sono ignorate le altre
                pressB = True
                # aggiorna per l'ultima volta il suo timer
                RGBtimeStrB = '%03.1f' % countDown
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
                    choiceColB = RGBColor[rispostaB]
                    if esitoB: # se ha indovinato si deve uscire dal ciclo
                        winB = True
                        oneguess = True
                        RGBtimeColorB = RGBtimeColWin
                        RGBscoreColorB = RGBscoreColWin
            # aggiornamento tempi dei due giocatori
            if not pressA: # aggiorna il tempo A se non ha premuto pulsanti
                if countDown <= 0:
                    RGBtimeStrA = '---'
                else:
                    RGBtimeStrA = '%03.1f' % countDown
            if not pressB: # aggiorna il tempo B se non ha premuto pulsanti
                if countDown <= 0:
                    RGBtimeStrB = '---'
                else:
                    RGBtimeStrB = '%03.1f' % countDown

            # scrivi sul display RGB composizione all'interno del ciclo del punto
            offline_matrix.Clear() # pulisce la matrice offline da comporre
            setRGBpart1()
            setRGBpart2()
            offline_matrix = matrix.SwapOnVSync(offline_matrix) # aggiorna il display

            # attesa, da tarare
            time.sleep(0.05)

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

        # esito del punto su console
        CSLesitoPnt()
        #time.sleep(0.5)

        # esito del punto su RGB
        offline_matrix.Clear() # pulisce la matrice offline da comporre
        #setRGBpart1()
        setRGBpart2()
        RGBesitoPnt() # sostituisce la parte 1
        offline_matrix = matrix.SwapOnVSync(offline_matrix) # aggiorna il display
        time.sleep(2.5)

        # esito della partita
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



