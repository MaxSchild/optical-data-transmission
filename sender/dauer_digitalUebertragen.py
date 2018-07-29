#dauer_digitalUebertragen.py
import time
import RPi.GPIO as GPIO


gpio_out = 2
GPIO.setmode(GPIO.BCM)
GPIO.setup(gpio_out, GPIO.OUT)
frequenz = int(input("Frequenz (Hz): ")) #Hz
nachrichtFaktor = int(input("Wie oft Nachricht? :"))
nachrichtString = input("Welche Nachricht?:")
nachrichtString *= nachrichtFaktor 
nachricht = []
binaryArray = []
outputWert = [0, 0, 0, 0, 0, 0, 0, 0]
outputWerteArray = []
zeitenArray = []

#nachricht umrechnen
for char in nachrichtString:
	ordnungsZahl = ord(char)
	nachricht.append(ordnungsZahl)
for number in nachricht:
	binNumber = bin(number)
	ersterBit = 8 - (len(binNumber) - 2)
	for j in range(0, len(binNumber) - 2): 
		outputWert[ersterBit + j] = int(binNumber[j + 2])
	binaryArray.append(outputWert)

#versenden

n = 0
while n < 1:
	currentTime = time.time()
	print("Kurz vor Kalibrierung")
	referenzZeit = time.time()
	GPIO.output(gpio_out, GPIO.HIGH)
	while currentTime < referenzZeit + 0.001:
		currentTime = time.time()
	GPIO.output(gpio_out, GPIO.LOW)
	while currentTime < referenzZeit + 0.001 + 0.001: 
		currentTime = time.time()
	GPIO.output(gpio_out, GPIO.HIGH)
	while currentTime < referenzZeit + 0.001 + 0.001 + 0.001 - 2 * (1 / frequenz):
		currentTime = time.time()
	#time.sleep(0.1)
	referenzZeit += 000.3 - (1 / frequenz)
	#print("Start!")
	zaehlerZeit = 1
	

	for j in binaryArray:
		#print("j", j)
		for k in j:
			#startTime = time.time()
			
			if k == False:
				currentTime = time.time()
				while currentTime < (referenzZeit + (1 / frequenz) * zaehlerZeit):
					currentTime = time.time()
				GPIO.output(gpio_out, GPIO.LOW)
			elif k == True:
				currentTime = time.time()
				while currentTime < (referenzZeit + (1 / frequenz) * zaehlerZeit):
					currentTime = time.time()
				GPIO.output(gpio_out, GPIO.HIGH)
			else:
				print("Was fuer ein mieser Fehler!")
			currentTime = time.time()
			zeitenArray.append(currentTime)
			zaehlerZeit += 1

			#time.sleep((1 / frequenz)-(currentTime - startTime))
	print("Fertig")
	#n += 1
	"""
for i in range(0, len(zeitenArray) - 1):
	print(zeitenArray[i+1] - zeitenArray[i])
	"""
	#print(len(zeitenArray))
	GPIO.output(gpio_out, GPIO.LOW)

	warten = input("Weiter? Wenn nicht dann 'n' zum Abbrechen")
	if warten == "n":
		GPIO.cleanup()
		break





