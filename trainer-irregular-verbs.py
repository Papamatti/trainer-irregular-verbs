#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#       trainer-irregular-verbs.py
#       
#       Copyright 1998-2014 CassieMoondust <cassie_lx@secure.mailbox.org>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 3 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.
#
#
#       This version is based on the QBASIC version which i've written during my
#       abitur - V1.22 in 16.12.1998
#       Hope, it is helpful for you

import random	# Zufallszahlen ermoeglichen
import sys
import os
import pickle

if sys.version_info.major < 3:
	print("Dieses Programm läuft ab Python3!")
	exit()

eingabezeile = sys.argv[1:]

#print(sys.argv)
#print(eingabezeile)

if '--nogui' in eingabezeile:
	nogui = True
else:
	nogui = False
	import tkinter as tk
	import tkinter.messagebox as tkmb

betriebssystem = sys.platform

##   Variablen-Beschreibungen

#   triazd - Anzahl Datensaetze
#   triwid - Defaultwert: Noetige Wiederholungen
#   trierc - Defaultwert: Fehlerzaehler
#   trilop - Defaultwert: Doppeltes Abfragen pro Durchlauf verhindern

#   SNnif1 - Hoechste noetigste Wiederholrate
#   SNhnw1 - maximale Durchlaeufe bei einem Verb

## Variablen und Tabllen definieren

version = "1.99.9"
prdatum = "13.07.2014"

debugger = False

SNFlag = 0		# Sniffer Ergebnisflag
SNlop3 = 1		# Loop-Bit (Wiederholungen verhindern)
SNlop33 = 0

sta1 = 0
sta2 = 0
sta3 = 0

EG1 = ""
EG2 = ""

PRFlag1 = 0
PRFlag2 = 0

triazd = 0		# Anzahl Datensaetze
#triwid = 0		# Wie oft schon abgefragt
#trierc = 0		# Gemachte Fehler
#trilop = 0		# Durchlaufzaehler

verbs = [ ["arise",			"arose",			"arosen"			],
		  ["awake",			"awoke", 			"awoken"			],
		  ["bear",			"bore",  			"borne" 			],
		  ["beat",			"beat",				"beaten"			],
		  ["become",		"became",			"become"			],
		  ["begin",			"began",			"begun"				],
		  ["bend",			"bent",				"bent"				],
		  ["bet",			"bet",				"bet"				],
		  ["bind",			"bound",			"bound"				],
		  ["bite",			"bit",				"bitten"			],
		  ["bleed",			"bled",				"bled"				],
		  ["blow",			"blew",				"blown"				],
		  ["break",			"broke",			"broken"			],
		  ["breed",			"bred",				"bred"				],
		  ["bring",			"brought",			"brought"			],
		  ["broadcast",		"broadcast",		"broadcast"			],
		  ["build",			"built",			"built"				],
		  ["burn",			"burnt/burned",		"burnt/burnded"		],
		  ["burst",			"burst",			"burst"				],
		  ["buy",			"bought",			"bought"			],
		  ["cast",			"cast",				"cast"				],
		  ["catch",			"cought",			"cought"			],
		  ["choose",		"chose",			"chosen"			],
		  ["cling",			"clung",			"clung"				],
		  ["come",			"came",				"come"				],
		  ["cost",			"cost",				"cost"				],
		  ["creep",			"crept",			"crept"				],
		  ["cut",			"cut",				"cut"				],
		  ["deal",			"dealt",			"dealt"				],
		  ["dig",			"dug",				"dug"				],
		  ["do",			"did",				"done"				],
		  ["draw",			"drew",				"drawn"				],
		  ["dream",			"dreamt/dreamed",	"dreamt/dreamed"	],
		  ["drink",			"drank",			"drunk"				],
		  ["drive",			"drove",			"driven"			],
		  ["eat",			"ate",				"eaten"				],
		  ["fall",			"fell",				"fallen"			],
		  ["feed",			"fed",				"fed"				],
		  ["feel",			"felt",				"felt"				],
		  ["fight",			"fought",			"fought"			],
		  ["find",			"found",			"found"				],
		  ["flee",			"fled",				"fled"				],
		  ["fly",			"flew",				"flown"				],
		  ["forbid",		"forbade",			"forbidden"			],
		  ["forecast",		"forecast",			"forecast"			],
		  ["forget",		"forgot",			"forgotten"			],
		  ["forgive",		"forgave",			"forgiven"			],
		  ["freeze",		"froze",			"frozen"			],
		  ["get",			"got",				"got"				],
		  ["give",			"gave",				"given"				],
		  ["go",			"went",				"gone"				],
		  ["grow",			"grew",				"grown"				],
		  ["hang",			"hung",				"hung"				],
		  ["hear",			"heard",			"heard"				],
		  ["hide",			"hid",				"hid/hidden"		],
		  ["hit",			"hit",				"hit"				],
		  ["hold",			"held",				"held"				],
		  ["hurt",			"hurt",				"hurt"				],
		  ["keep",			"kept",				"kept"				],
		  ["kneel",			"knelt/Kneeled",	"knelt/kneeled"		],
		  ["knit",			"knit",				"knit/knitted"		],
		  ["know",			"knew",				"known"				],
		  ["lay",			"laid",				"laid"				],
		  ["lead",			"led",				"led"				],
		  ["lean",			"leant/leaned",		"leant/leaned"		],
		  ["leap",			"leapt/leaped",		"leapt/leaped"		],
		  ["learn",			"learnt/learned",	"learnt/learned"	],
		  ["leave",			"left",				"left"				],
		  ["lend",			"lent",				"lent"				],
		  ["let",			"let",				"let"				],
		  ["lie",			"lay",				"lain"				],
		  ["light",			"lit/lighted",		"lit/lighted"		],
		  ["loose",			"lost",				"lost"				],
		  ["make",			"made",				"made"				],
		  ["mean",			"meant",			"meant"				],
		  ["meet",			"met",				"met"				],
		  ["pay",			"paid",				"paid"				],
		  ["put",			"put",				"put"				],
		  ["read",			"read",				"read"				],
		  ["ride",			"rode",				"ridden"			],
		  ["ring",			"rang",				"rung"				],
		  ["rise",			"rose",				"risen"				],
		  ["run",			"ran",				"run"				],
		  ["saw",			"sawed",			"sawn/sawned"		],
		  ["say",			"said",				"said"				],
		  ["see",			"saw",				"seen"				],
		  ["seek",			"sought",			"sought"			],
		  ["sell",			"sold",				"sold"				],
		  ["send",			"sent",				"sent"				],
		  ["set",			"set",				"set"				],
		  ["sew",			"sewed",			"sewn/sewned"		],
		  ["shake",			"shook",			"shaken"			],
		  ["shine",			"shone",			"shone"				],
		  ["shoot",			"shot",				"shot"				],
		  ["show",			"showed",			"shown"				],
		  ["shrink",		"shrank",			"shrunk"			],
		  ["shut",			"shut",				"shut"				],
		  ["sing",			"sang",				"sung"				],
		  ["sink",			"sank",				"sunk"				],
		  ["sit",			"sat",				"sat"				],
		  ["sleep",			"slept",			"slept"				],
		  ["smell",			"smelt/smelled",	"smelt/smelled"		],
		  ["sow",			"sowed",			"sown/sowed"		],
		  ["speak",			"spoke",			"spoken"			],
		  ["speed",			"sped",				"sped"				],
		  ["spend",			"spent",			"spent"				],
		  ["spin",			"spun",				"spun"				],
		  ["spit",			"spat",				"spat"				],
		  ["split",			"split",			"split"				],
		  ["spoil",			"spoilt/spoiled",	"spoilt/spoiled"	],
		  ["spread",		"spread",			"spread"			],
		  ["spring",		"sprang",			"sprung"			],
		  ["stand",			"stood",			"stood"				],
		  ["steal",			"stole",			"stolen"			],
		  ["stick",			"stuck",			"stuck"				],
		  ["sting",			"stung",			"stung"				],
		  ["stink",			"stank",			"stunk"				],
		  ["strike",		"struck",			"struck"			],
		  ["swear",			"swore",			"sworn"				],
		  ["sweep",			"swept",			"swept"				],
		  ["swim",			"swam",				"swum"				],
		  ["swing",			"swung",			"swung"				],
		  ["take",			"took",				"taken"				],
		  ["teach",			"taught",			"taught"			],
		  ["tear",			"tore",				"torn"				],
		  ["tell",			"told",				"told"				],
		  ["think",			"thought",			"thought"			],
		  ["throw",			"threw",			"thrown"			],
		  ["thrust",		"thrust",			"thrust"			],
		  ["understand",	"understood",		"understood"		],
		  ["wake",			"woke",				"woken"				],
		  ["wear",			"wore",				"worn"				],
		  ["weep",			"wept",				"wept"				],
		  ["win",			"won",				"won"				],
		  ["wind",			"wound",			"wound"				],
		  ["withdraw",		"withdrew",			"withdrawn"			],
		  ["write",			"wrote",			"written"			] ]

## Systemcheck. Das Programm läuft derzeit nur mit Linux.

if not "linux" in betriebssystem:
	print ("Soryy, Linux only!")
	exit()

## trivia - Statistik-Tabelle erzeugen.
#  Hier wird geprüft, ob bereits eine Datei vorhanden ist in der die
#  Statistiken gespeichert wurden, wenn nicht wird eine neue Tablle
#  erzeugt.
#  Die Tabelle speichert für jedes Verb drei Zahlenwerte
#  Feld 0: Noetige Wiederholungen
#  Feld 1: Fehlerzaehler
#  Feld 2: Doppeltes Abfragen verhindern
#		   (1 wenn schon abgefragt, 0 wenn noch nicht)

triazd = len(verbs)
#triazd = 4
	

trivia = []
#if "linux" in sys.platform:
if os.path.exists("iverbs.dat") and os.access(r'iverbs.dat',2):
	if debugger: print ("yes")
	with open('iverbs.dat','rb') as datei:
		trivia = pickle.load(datei)
		
	#datei = open("iverbs.dat","rb")
	#trivia = pickle.load(datei,fix_imports=True)
	#datei.close()
else:
	for i in range(triazd):
		trivia.append([0,0,0])
	if debugger: print ("nöö")
	

## FUNKTIONSDEFINITIONEN

def titleTerm(version,prdatum):
	# Hier die Textversion
	os.system('cls' if os.name=='nt' else 'clear')
	print (" ________________________________________ ")
	print ("|                                        |")
	print ("|       Trainer: Irregular verbs         |")
	print ("|     Version", version, " (", prdatum, ")     |")
	print ("|________________________________________|\n")
		
def fenster():
	global root, logo, version, prdatum, status
	# Tkinter GUI erstellen
	root = tk.Tk()
	root.geometry("400x400")
	root.protocol("WM_DELETE_WINDOW", saveprefs)  # Schliessen Button ruft Funktion saveprefs() auf.
	root.title("Trainer: Irregular verbs")
	logo = tk.PhotoImage(file="UK_Flag.ppm")
	tk.Label(root, padx=2, pady=2, image=logo).pack(padx=10, pady=15, side="top")
	tk.Button(root, text="About", command=AboutWindow).pack(side="top", padx=25, pady=10)
	# Statuszeile definieren und Daten anzeigen.
	status = tk.Label(root, text="", bd=1, relief="sunken", anchor="w")
	status.pack(side="bottom", fill="x")
	stati()
	
def makeform(root, eingabefelder):
	texteingaben = []
	for field in eingabefelder:
		row = tk.Frame(root)
		lab = tk.Label(row, width=15, text=field, anchor='w')
		ent = tk.Entry(row)
		row.pack(side='top', fill='x', padx=5, pady=5)
		lab.pack(side='left')
		ent.pack(side='right', expand='yes', fill='x')
		texteingaben.append((field, ent))  
	return texteingaben

def AboutWindow():
	global root,version,prdatum
	explanation = "Trainer: Irregular verbs\nVersion " + version + " (" + prdatum + ")\n\n(c) 1998-2013 Cassandra Freund\nLizenz: GPLv3 oder höher"
	tkmb.showinfo('Über dieses Programm', explanation)
	return

def sniffer():
	#Sucht ein Verb mit hoechster Lernprioritaet
	global SNFlag, trivia, SNlop33, debugger
	
	SNFlag = -1		# Sniffer Ergebnisflag zuruecksetzen
	SNnif  = 0		# Hoechste noetigste Wiederholrate
	SNhnw  = 0		# maximale Durchlaeufe bei einem Verb
	SNlop  = 1		# Loop-Bit (Wiederholungen verhindern)
	SNanz = []		# Positionstabelle der noch nicht durchgenommenen Verben
		
	# Ausnahmefall: Muss ein Verb sofort wiederholt werden?
	# Wenn ja: Wort auswaehlen und zurueck zum Hauptprogramm.
	for z1 in range(triazd):
		if trivia[z1][2] == -1:
			SNFlag = z1
			break
	if debugger: print ("SNFlag after break", SNFlag)
		
	if SNFlag == -1:
		if debugger: print ("Nullschleife betreten")

		# Wurden bereits alle Verben einmal durchgekaut?
		SNlop = 1		# Loop-Bit (Wiederholungen verhindern)
		for z1 in range(triazd):
			if trivia[z1][2] == 0:
				SNlop = 0
				SNanz.append(z1)
	
		# Loop-Flag zuruecksetzen falls alle Verben Abgefragt wurden
		if SNlop == 1:
			for z1 in range(triazd):
				trivia[z1][2] = 0
	
		# Maximale Durchlaeufe bei einem Verb finden
		for z1 in range(triazd):
			if trivia[z1][0] > SNhnw:
				SNhnw = trivia[z1][0]
		if debugger: print ("Maximale Durchlaeufe:SNhnw=",SNhnw)
	
		# Suche die kleinste gemeinsame Anzahl der Wiederholungen
		SNnif = SNhnw
		for z1 in range(triazd):
			if trivia[z1][0] < SNnif and trivia[z1][2] == 0:
				SNnif = trivia[z1][0]
		if debugger: print ("Kleinste Anzahl Wiederholungen:SNnif=",SNnif)
		
		# Erstelle eine Tabelle mit den Verben, die am wenigsten abgefragt wurden
		SNless = []
		for z1 in range(triazd):
			if trivia[z1][0] == SNnif:
				SNless.append(z1)
		if debugger == 1:
			print ("Abfragetabelle",SNless)
	
		# Suche zufaellig ein Verb heraus das noch nicht wiederholt wurde
		# und am wenigsten Durchlaeufe aufweist!
		#while trivia[z1][0] >= SNnif:
			# z1 = random.randint(1, triazd) - 1
		z1 = random.choice(SNless)
		SNFlag = z1
		if debugger: print ("Zufall",SNFlag)

def eingabe_nogui():
	global EG1,EG2,eingabefelder
	EG1 = ""
	EG2 = ""
	keinedaten = True
	while keinedaten:
		print("\nDas Verb in der Grundform lautet: ",color.GREEN, color.BOLD, verbs[SNFlag][0], color.END)
		print("\nGib bitte die fehlenden Zeitformen korrekt ein!\n")
		EG1 = input("- past simple   ? ")
		EG2 = input("- past perfect  ? ")
		if len(EG1) == 0 and len(EG2) == 0:
			title()
			print ("\nGib bitte etwas ein!\n")
		else:
			keinedaten = False

def eingabe_gui():
	global EG1,EG2,root,eingabefelder,nogui
	EG1 = ""
	EG2 = ""
	dasgesuchtewort = str(verbs[SNFlag][0])
	tk.Label(root, text="Das Verb in der Grundform lautet: ").pack(padx=5, pady=5)
	tk.Label(root, text=dasgesuchtewort, justify = 'left', compound = 'left', fg = "light green", bg = "dark green",).pack()
	
	tk.Label(root, text="Gib bitte die fehlenden Zeitformen korrekt ein!").pack(pady=10)
	
	ents = makeform(root, ['past simple', 'past perfect'])
	# Reagieren auf die Return Taste und auf den Enter-Button:
	root.bind('<Return>', (lambda event, e=ents: verarbeitung(e))) 
	tk.Button(root, text="Enter", command=(lambda e=ents: verarbeitung(e))).pack(side="top", padx=5, pady=25)
	#tk.Button(root, text="Quit" , command=saveprefs).pack(side="left", padx=5, pady=10)
	tk.Button(root, text="About", command=AboutWindow).pack(side="right", padx=5, pady=10)
	
def verarbeitung(entries):
	global root,EG1,EG2,trivia,PRFlag1,PRFlag2,sta1,sta2,sta3,nogui,debugger
	EG1e = entries[0]
	EG2e = entries[1]
	if debugger: print (EG1e)
	if debugger: print (EG2e)
	EG1 = EG1e[1].get()
	EG2 = EG2e[1].get()
	if debugger: print ("EG1: ",EG1," EG2: ",EG2)

	## Der alte Code:
	#for entry in entries:
	#	field = entry[0]
	#	text = entry[1].get()
	#	if debugger == 1: print('%s: "%s"' % (field, text))

	professor()
	mahnman()
	stati()

def professor():
	global trivia, PRFlag1, PRFlag2
	
	# Sind zwei Variablen moeglich? (Getrennt durch "/"),
	# falls vorhanden Menge der Teiler, ansonsten 0
	PRsms2 = 0
	PRsms3 = 0
	
	# Falls mehrere Moeglichkeiten existieren wird die Variable geteilt
	# und in folgende Variablen gespeichert!
	PRvar2 = []
	PRvar3 = []
		
	# Zaehler fuers Wort hochsetzen
	# (Ausnahme: wenn das Wort nach Fehleingabewiederholt eingegeben
	# werden muss!)
	if trivia[SNFlag][2] > -1:
		trivia[SNFlag][0] += 1
	
	# Sind zwei Formen moeglich? (durch "/" getrennt)
	if "/" in verbs[SNFlag][1]:
		PRvar2 = verbs[SNFlag][1].split("/")
		PRsms2 = len(PRvar2)
		
	if "/" in verbs[SNFlag][2]:
		PRvar3 = verbs[SNFlag][2].split("/")
		PRsms3 = len(PRvar3)
	
	# Pruefung der Verben auf Richtigkeit (PRFlag1 und 2 sind global)
	PRFlag1 = 0
	if PRsms2 > 0:
		if EG1 == PRvar2[0] or EG1 == PRvar2[1]:
			PRFlag1 = 1
	else:
		if EG1 == verbs[SNFlag][1]:
			PRFlag1 = 1
	
	PRFlag2 = 0
	if PRsms3 > 0:
		if EG2 == PRvar3[0] or EG2 == PRvar3[1]:
			PRFlag2 = 1
	else:
		if EG2 == verbs[SNFlag][2]:
			PRFlag2 = 1
	
	# Bewertung und ggf. Loop-Bit zuruecksetzen
	if PRFlag1 != 1 or PRFlag2 !=1:
		trivia[SNFlag][1] += 1
		trivia[SNFlag][2] = -1
	else:
		if trivia[SNFlag][2] == -1:
			trivia[SNFlag][2] = 0
		else:
			trivia[SNFlag][2] = 1

def mahnman():
	global root, PRFlag1, PRFlag2, nogui
	
	if PRFlag1 != 1:
		mahnung1 = "\nDie Antwort für Past Simple war:  FALSCH! Richtig währe " + verbs[SNFlag][1] + " gewesen.\n"
		#print("FALSCH! Richtig währe:", verbs[SNFlag][1])
	else:
		mahnung1 = "\nDie Antwort für Past Simple war:  RICHTIG!"
		#print("RICHTIG!")
	if PRFlag2 != 1:
		mahnung2 = "Die Antwort für Past Perfect war: FALSCH! Richtig währe " + verbs[SNFlag][2] + " gewesen.\n"
		#print("FALSCH! Richtig währe:", verbs[SNFlag][2])
	else:
		mahnung2 = "Die Antwort für Past Perfect war: RICHTIG!"
		#print("RICHTIG!")
	
	if nogui:
		print ("\n", mahnung1)
		print (mahnung2)
	else:
		ausgabezeile = mahnung1 + "\n\n" + mahnung2
		tkmb.showwarning("Hinweis", ausgabezeile)
	
def stati():
	global sta1, sta2, sta3, nogui, status, root, debugger
	sta1 = 0
	sta2 = 0
	sta3 = 0
	for z1 in range(triazd):
		sta1 = sta1 + trivia[z1][0]
		sta2 = sta2 + trivia[z1][1]
	if sta1 > 0:
		# Division by zero verhindern.
		ergebnis = (sta2 * 100) / sta1
		if ergebnis > 100: ergebnis = 100
		sta3 = int(ergebnis)
	
	if nogui:
		print ("") # Irgendwie sehen die Linien anders aus wenn \n in der gleich Zeile eingefuegt wird.
		print ("–––––––––––––––––––––––––––––––––––––––––––––––––––")
		if debugger: print (" Status:", trivia[SNFlag][0], ",",trivia[SNFlag][1],",",trivia[SNFlag][2])
		print (" Bisherige Durchläufe: ",sta1,"             ")
		print (" Bisherige Fehler    : ",sta2,"             ")
		print (" Fehlerquote         : ",sta3,"%            ")
		print ("___________________________________________________\n")
	else:
		ausgabezeile = "Durchläufe: " + str(sta1) + " Fehler: " + str(sta2) +" Quote: " + str(sta3) + "%"
		status.config(text=ausgabezeile)
		status.update_idletasks()
		#tkmb.showwarning("Auswertung", ausgabezeile)

def saveprefs():
	global trivia, nogui, root
	with open('iverbs.dat', 'wb') as datei:
		pickle.dump(trivia, datei)
	datei.close()
	print ("Datei geschlossen:",datei.closed)
	exit()
	#datei = open("iverbs.dat","w")
	#pickle.dump(trivia,datei)
	#datei.close()
	if nogui:
		exit()
	else:
		root.destroy
	
class color:
	PURPLE = '\033[95m'
	CYAN = '\033[96m'
	DARKCYAN = '\033[36m'
	BLUE = '\033[94m'
	GREEN = '\033[92m'
	YELLOW = '\033[93m'
	RED = '\033[91m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'
	END = '\033[0m'
      

## So, endlich: Das Hauptprogramm!
# Allerdings geteilt in GUI und NICHTGUI Varienten

if nogui:
	# Textmodus-Variante
	zuende = 'j'
	while zuende.lower() == 'j':
		titleTerm(version,prdatum)
		sniffer()
		eingabe_nogui()
		professor()
		mahnman()
		stati()
		zuende = input("Weitermachen (j/n)? ")
	saveprefs()
else:
	## Beschreibung der GUI-Variante mit Tkinter.
	# Nach dem Druecken der Return/Enter Taste oder klicken auf den "Enter-Button"
	# wird die Funktion verarbeitung() aufgerufen, welche die Eingabe entgegennimmt
	# und nacheinander die Funktionen professor(), mahnman() und stati() aufruft.
	# Wird das Fenster geschlossen wird die Funktion Saveprefs() aufgerufen und die
	# Daten mit saveprefs() geschrieben.
	fenster()
	sniffer()
	eingabe_gui()
	root.mainloop()

## ENDE
