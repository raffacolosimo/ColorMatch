#!/usr/bin/env python

print 'inizio'
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
import time

print 'librerie importate'

options = RGBMatrixOptions()
options.hardware_mapping = 'adafruit-hat'
options.rows = 32
options.chain_length = 2

matrix = RGBMatrix(options = options)
offscreen_canvas = matrix.CreateFrameCanvas()
print 'matrice creata'
font1 = graphics.Font()
font2 = graphics.Font()
font3 = graphics.Font()
font4 = graphics.Font()
font1.LoadFont("./fonts/6x10.bdf")
font2.LoadFont("./fonts/10x20.bdf")
font3.LoadFont("./fonts/4x6.bdf")
font4.LoadFont("./fonts/9x18.bdf")
print 'font caricati'

#TESTO1
posH = 0
posV = 7 
text = '-BLU-'
color = graphics.Color(255, 0, 0)
graphics.DrawText(offscreen_canvas, font1, posH, posV, color, text)
#TESTO2
posH = 34
posV = 7 
text = 'ROSSO'
color = graphics.Color(0, 255, 0)
graphics.DrawText(offscreen_canvas, font1, posH, posV, color, text)
#TESTO3
posH = 17
posV = 16 
text = 'VERDE'
color = graphics.Color(0, 0, 255)
graphics.DrawText(offscreen_canvas, font1, posH, posV, color, text)

#MARKER
def marker(mrkposH, mrkposV, mrkL, mrkH, mrkcol):
	lineEndX = mrkposH + mrkL
	for i in range(mrkH):
		lineY = mrkposV - i
		graphics.DrawLine(offscreen_canvas, mrkposH, lineY, lineEndX, lineY, mrkcol)
posH = 27
posV = 31 
#text = '*'
color = graphics.Color(0, 0, 255)
marker(posH, posV, 8, 14, color)

#TIME Sx
posH = 14
posV = 27 
timeSx = 5
text = '%03.1f' % timeSx
color  = graphics.Color(180, 180, 180)
graphics.DrawText(offscreen_canvas, font3, posH, posV, color, text)
#TIME Dx
posH = 39 
timeDx = 5
text = '%03.1f' % timeDx
graphics.DrawText(offscreen_canvas, font3, posH, posV, color, text)

#SCORE Sx
posH = 0
posV = 29 
text = '1'
color  = graphics.Color(255, 255, 255)
graphics.DrawText(offscreen_canvas, font4, posH, posV, color, text)
#SCORE Dx
posH = 56 
text = '0'
graphics.DrawText(offscreen_canvas, font4, posH, posV, color, text)

def choice(side, color):
	if side=='Sx':
		marker(0,16, 7, 4, color)
	elif side=='Dx':
		marker(56,16, 7, 4, color)
	else:
		print 'errore'

print 'schermata pronta'
offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)

time.sleep(0.1)
pointover=False
gameover =False

while timeSx > 0:
	offscreen_canvas.Clear()

	#TESTI
	#TESTO1
	posH = 0
	posV = 7 
	text = '-BLU-'
	color = graphics.Color(255, 0, 0)
	graphics.DrawText(offscreen_canvas, font1, posH, posV, color, text)
	#TESTO2
	posH = 34
	posV = 7 
	text = 'ROSSO'
	color = graphics.Color(0, 255, 0)
	graphics.DrawText(offscreen_canvas, font1, posH, posV, color, text)
	#TESTO3
	posH = 17
	posV = 16 
	text = 'VERDE'
	color = graphics.Color(0, 0, 255)
	graphics.DrawText(offscreen_canvas, font1, posH, posV, color, text)

	#MARKER
	posH = 27
	posV = 31 
	#text = '*'
	#graphics.DrawText(offscreen_canvas, font2, posH, posV, color, text)
	marker(posH, posV, 8, 14, color)

	#SCORE Sx
	posH = 0
	posV = 29 
	text = '1'
	color  = graphics.Color(255, 255, 255)
	graphics.DrawText(offscreen_canvas, font4, posH, posV, color, text)
	#SCORE Dx
	posH = 56 
	text = '0'
	graphics.DrawText(offscreen_canvas, font4, posH, posV, color, text)


	#TIME Sx
	posH = 14
	posV = 27 

	if timeSx > 0: 
		text = '%03.1f' % timeSx 
		if text == '3.9': # simulazione di scelta errata
			colorSx = graphics.Color(255, 0, 0)
			choice('Sx', colorSx)
			color  = graphics.Color(80, 80, 80)
			graphics.DrawText(offscreen_canvas, font3, posH, posV, color, text)
			graphics.DrawLine(offscreen_canvas, posH, posV+1, posH+10, posV+1, color)
		else:
			color  = graphics.Color(180, 180, 180)
			timeSx -= 0.05
			graphics.DrawText(offscreen_canvas, font3, posH, posV, color, text)
	else: 
		text = '---'
		graphics.DrawText(offscreen_canvas, font3, posH, posV, color, text)
		pointover=True
	#TIME Dx
	posH = 39 
	if timeDx > 0: 
		text = '%03.1f' % timeDx 
		if text == '3.3': # simulazione di scelta giusta
			colorDx = graphics.Color(0, 0, 255)
			choice('Dx', colorDx)
			color  = graphics.Color(255, 255, 255)
			graphics.DrawText(offscreen_canvas, font3, posH, posV, color, text)
			graphics.DrawLine(offscreen_canvas, posH, posV+1, posH+10, posV+1, color)
			pointover=True
		else:
			color  = graphics.Color(180, 180, 180)
			timeDx -= 0.05
			graphics.DrawText(offscreen_canvas, font3, posH, posV, color, text)
	else: 
		text = '---'
		graphics.DrawText(offscreen_canvas, font3, posH, posV, color, text)

	time.sleep(0.1)
	offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)
	if pointover:
		break

	
time.sleep(5)

