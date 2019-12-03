#BLE_serial_programmer

#pyserial module
import serial
import serial.tools.list_ports
import os

clear = lambda: os.system('cls')
clear()

DefaultPort = 'COM1'
DefaultBaud = 38400
timeout = 1

ser = serial.Serial(port = DefaultPort, baudrate=38400, bytesize=8, timeout=1, stopbits=serial.STOPBITS_ONE, parity=serial.PARITY_NONE)

def main():
	Init()
	#input('Drücke ENTER zum starten!\n')
	PortSel()
	Standby()
	input('Press ENTER to exit')
	
def Init():
	print('\n\n_______________BLE Programmierer - Adrian Schwizgebel_________________________\n\n')
	print('Diese Software dient zum Programmieren der Seriennummern für die BLE-Module\nder e8-Schweissgeräte.\n')
	print('Zu Beginn müssen Sie jeweils den COM-Port auswählen, an welchem der\nUSB-zu-Seriell-Programmierer angeschlossen ist.')
	print('\nFalls der Port nicht bekannt ist, finden Sie diesen im Windows Geräte-Manager\nunter <Anschlüsse> als "Profilic USB-to-Serial Comm Port".')
	print('\n\nStarten Sie die Software nun mit der Eingabe von ENTER.')
	input()
	
def Standby():
	clear()
	print('\n\n_______________BLE Programmierer - Menu_______________________________________\n\n')
	print('Benutze <manuell> um manuell eine Serienummer zu programmieren.')
	print('Benutze <start> um fortlaufende Serienummern zu programmieren.\n\n')
	KeyboardInput = input()
	if KeyboardInput == 'help':
		OpenHelp()
	elif KeyboardInput == 'manual' or KeyboardInput == 'manuell':
		clear()
		print('\n\n_______________BLE Programmierer - Manuelle Programmierung____________________\n\n')
		GetSerial()
		Standby()
	elif KeyboardInput == 'start':
		clear()
		print('\n\n_______________BLE Programmierer - Fortlaufende Programmierung________________\n\n')
		AutoWriteSerialStart()
		Standby()
	elif KeyboardInput == 'port':
		PortSel()
		Standby()
	elif KeyboardInput == 'exit':
		clear()
		ser.close()
		exit()
	elif KeyboardInput == '':
		Standby()
	else:
		Standby()
	
def OpenHelp():
	clear()
	print('\n\n_______________BLE Programmierer - Hilfe______________________________________\n\n')
	print('Benutze <manual> um manuell eine Serienummer zu programmieren.')
	print('Benutze <start> um fortlaufende Serienummern zu programmieren.')
	print('Benutze <port> um den Serial-Port zu wechseln.')
	print('Benutze <back> oder <menu> um zum Hauptmenu zurück zu kehren.')
	print('Benutze <exit> um Programm zu schliessen.')
	input('\nBeende Hilfe mit beliebiger Eingabe.\n\n')
	Standby()
	
def PortSel():
	clear()
	foundPortflag = 0
	print('\n\n_______________BLE Programmierer - Port auswählen_____________________________\n\n')
	if ser.isOpen():
		ser.close()
	print('Folgende COM-Ports wurden entdeckt:\n')
	ports = serial.tools.list_ports.comports()
	for port, desc, hwid in sorted(ports):
		print("{}\t: {}".format(port, desc))
		if "Prolific" in desc:
			ser.port = port
			foundPortflag = 1
	if foundPortflag == 0:
		temp = input('\nGewünschten Port eingeben und mit ENTER bestätigen.\nFür Standart-Port <' + DefaultPort + '> leer lassen:\n\n')
		if temp == '':
			ser.port = DefaultPort
			print('Standart-Port <' + DefaultPort + '> ausgewählt.\n')
		else:
			if "COM" in temp:
				ser.port = temp
				#print('Port <' + ser.port + '> ausgewählt.')
			else:
				print('Verwende das Format: COM[nr]')
				input()
				PortSel()
	OpenPort()
	
def OpenPort():
	if ser.isOpen():
			print('\n<' + ser.name + '> ist bereits geöffnet.\n')
	else:
		ser.open()
		if ser.isOpen():
			print('\n<' + ser.name + '> ausgewählt und geöffnet.\n')
		else:
			print('\nKonnte Port <' + str(ser.name) + '> nicht öffnen.\n')
	
def GetSerial():
	serialnr = input('Serienummer eingeben und mit ENTER bestätigen!\n\nSerienummer: ')
	if not serialnr.isdigit():
		if serialnr == 'menu' or serialnr == 'back':
			Standby()
		else:
			print('Keine gültige Eingabe.')
			GetSerial()
	else:
		if len(str(serialnr)) == 6:
			serialnr = int(serialnr)
			WriteSerial(serialnr)
			GetSerial()
		else:
			print('Kein gültige Eingabe.')
			GetSerial()
	
def AutoWriteSerialStart():
	serialnr = input('Serienummer eingeben und mit ENTER bestätigen!\n\nSerienummer: ')
	if not serialnr.isdigit():
		if serialnr == 'menu' or serialnr == 'back':
			Standby()
		else:
			print('Keine gültige Eingabe.')
			AutoWriteSerialStart()
	else:
		if len(str(serialnr)) == 6:
			serialnr = int(serialnr)
			WriteSerial(serialnr)
			AutoWriteSerialLoop(serialnr)
		else:
			print('Kein gültige Eingabe.')
			AutoWriteSerialStart()
	
def AutoWriteSerialLoop(previousSerial):
	tempInput = input('Nächste Serienummer ' + str(previousSerial + 1) + ' mit ENTER bestätigen!')
	if tempInput == '':
		serialnr = previousSerial + 1
		WriteSerial(serialnr)
		AutoWriteSerialLoop(serialnr)
	else:
		Standby()
	
def WriteSerial(serialnr):
	fixPacketPart = [0x02, 0x11, 0x07, 0x00, 0x16]
	packet = bytearray()
	
	# fix part
	packet.extend(fixPacketPart)
	
	# serial-nr part
	for character in str(serialnr):
		packet.append(int(character.encode('latin-1')) + 48)
	
	# parity part
	parity = 2
	for byte in range(5,11):
		parity = parity ^ packet[byte]
	packet.append(parity)

	if ser.isOpen():
		ser.write(packet)
		SerialBytes = packet
		print('Serienummer <' + str(serialnr) + '> gesendet an <' + str(ser.name) + '>.\n')
	elif not ser.isOpen():
		print('Kein Port offen.')
main()