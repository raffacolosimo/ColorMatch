from gpiozero import LED, Button
import time

button_a = Button(14) # rosso
button_b = Button(15) # verde
button_c = Button(18) # blu
print 'Premi un pulsante'
while True:
	while True:
		if button_a.is_pressed or button_b.is_pressed or button_c.is_pressed:
			if button_a.is_pressed:
				risposta=0
			elif button_b.is_pressed:
				risposta=1
			else:
				risposta=2
			break
	print 'Hai premuto il pulsante ' + str(risposta) 
	print 'Attendi...'
	time.sleep(0.5)
	print 'Ok, riprova'

