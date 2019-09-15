""" Pokemon quiz """

from sys import exit
from os import system
from time import time

class Quiz():
	"""
	Quiz-classen som er ansvarlig for å kjøre quizen. Inneholder funksjonene
	- _Språk som bestemmer språk for quizen
	- _Region bestemmer regioner som skal tas i bruk
	- _Start_Timer starter en tidtagning
	- _Skaff_Pokemon leser pokedexen og henter alle pokemon, deres nummere og typer, som tilhører regionene bestemt av _Region
	- _Print_oppsett printer det generelle oppsettet av quizen. Printer også sluttoppsettet hvis kalt med variabelen "alt = True"
	- _Exit avslutter quizen ved å printe fullstendig oppsett og tiden brukt
	- _Riktig_svar fikse å oppdatere lister hvis riktige svar blir gitt
	- Programmet kaller på de andre funksjonene og inneholder selve løkka som driver quizen.
	"""
	
	def __init__(self):
		"""
		Definerer en del forskjellige konstanter.
			- Hint er variabel som slår på printing av typen Pokemon
			- Korrekte er en teller for antall korrekte svar gitt
			- Alle_regioner er en liste med navn på alle regioner som er støttet
			- Alle_språk er en liste med alle språk støttet. Og deres forskjellige stavemåter som funker
			- Språk er en variabel for hvilket språk som er valgt. -1 er ingen, 0 er norsk, 1 er engelsk
		"""
		
		self.Hint			= False
		self.Korrekte		= 0
		self.Alle_regioner	= ["Test", "Kanto", "Johto", "Hoenn", "Sinnoh"]
		self.Alle_språk		= ["Norsk", "norsk", "Norwegian", "norwegian", "Engelsk", "engelsk", "English", "english"]
		self.Språk = -1
	
	def _Språk(self):
		"""
		Spør om språk fra bruker og setter dette språket for senere funksjoner. 
		Takler feilgitte språk ved å spørre på nytt.
		"""
		
		# Spør om språk
		Språk = input("What language do you want? Hvilket språk ønsker du? ")
		
		# Sjekker om dette er et støttet språk og spør på nytt hvis ikke
		while Språk not in self.Alle_språk:
			if Språk in ["Exit", "exit", "Quit", "quit", "Slutt", "slutt", "Avslutt", "avslutt"]:
				exit()
			print("The language %s doesn't exist or is not supported by this quiz. Choose between %s or %s"%(Språk, self.Alle_språk[2], self.Alle_språk[6]))
			print("Språket %s eksisterer ikke, eller støttes ikke av denne quizen. Velg mellom %s eller %s."%(Språk, self.Alle_språk[1], self.Alle_språk[5]))
			Språk = input("What language do you want? Hvilket språk ønsker du? ")
		
		# Setter variabelen self.Språk som er den som brukes senere
		if Språk in self.Alle_språk[0:4]: 
			self.Språk = 0
		elif Språk in self.Alle_språk[4:8]:
			self.Språk = 1
	
	def _Region(self):
		"""
		Spør bruker om hvilke regioner som skal tas med i quizen.
		Takler bindeord ved å fjerne disse.
		Kan ta imot alle/all for at alle regioner skal brukes.
		Takler feilgitte språk ved å spørre på nytt.
		"""
		
		# Setter språk
		if self.Språk == 0:
			input_tekst = "Hvilke(n) region(er) ønsker du? "
		elif self.Språk == 1:
			input_tekst = "What/which region(es) whould you like? "
		else:
			print("# No language has been choosen. Ending quiz #")
			exit()
		
		# Spør om region
		Region = input(input_tekst).split()
		
		bindeord = ["And", "and", "Og", "og"]
		indekser = []
		
		# Fjerner eventuelle bindeord og komma fra brukerinput
		for i in range(len(Region)):
			if Region[i] in bindeord: # Finner indeksen til bindeord i streng
				indekser.append(i)
			elif Region[i][-1] == ",": # Fjerner komma i streng
				Region[i] = Region[i][:-1]
		for i in indekser: # Fjerner bindeord i streng
			Region.pop(i)
		
		indekser = []
		
		# Fikser om regionsnavn ble gitt feil
		for i in range(len(Region)):
			while Region[i] not in self.Alle_regioner:
				if Region in ["Exit", "exit", "Quit", "quit", "Slutt", "slutt", "Avslutt", "avslutt"]:
					exit()
				elif Region[i] in ["Alle", "alle", "All", "all"]: # Fikser alle som input
					Region = self.Alle_regioner.pop(0)
				elif Region[i] in ["Ingen", "ingen", "Non", "non", "Nei", "nei", "No", "no"]: # Fikser fjerning av region
					indekser.append(i)
					Region[i] = "Kanto"
				else: # Spør om ny region hvis en av de gitte var feil
					if self.Språk == 0:
						print("Regionen %s eksisterer ikke, eller er for ny. Velg en annen."%Region[i])
						Region[i] = input(input_tekst).split()[0]
					elif self.Språk == 1:
						print("The region %s doesn't exist or is too new. Choose another."%Region[i])
						Region[i] = input(input_tekst).split()[0]
		for i in indekser: # Fjerner uønskede reginonsnavn i streng
			Region.pop(i)
		
		# Gjør region til en klassevariabel
		self.Region = Region
		
	def _Start_Timer(self):
		"""
		Starter timer
		"""
		
		self.start_tid = time()
	
	def _Skaff_Pokemon(self):
		"""
		Kaller på _Region, åpner og henter inn info fra Pokedex.txt og defienrer denne informasjonen som klassevariabler
		"""
		
		self._Region()
		
		with open("Pokedex.txt", "r") as innfil: # Åpner Pokedex for lesing
			# Etablerer lister som skal fylles
			Tallene			= []
			Navna 			= []
			Typene 			= []
			Korrekte_navn	= []
			
			for i in range(2): # Hopper over de to første linjene
				innfil.readline()
			
			# Henter infoen som trengs, linje for linje
			for linje in innfil:
				if len(linje.split()) <= 1: # Hopper over tomme linjer
					False
				
				elif linje.split()[1] in self.Alle_regioner: # Lagrer hvilken region de neste pokemonene er fra
					midl = linje.split()[1]
				
				elif midl in self.Region: # Lagrer info hvis linja ikke inneholder region eller er blank, men regionen skal brukes
					Tall	= linje.split()[0]
					Navn	= linje.split("\t\t")[0][4:]
					
					if len(linje.split()) >= 4:
						Type1	= linje.split()[-2]
						Type2 = linje.split()[-1]
					
					else:
						Type1	= linje.split()[-1]
						Type2 = " "
					
					Tallene.append(int(Tall))
					Navna.append(Navn)
					Typene.append([Type1, Type2])
					Korrekte_navn.append(" ")
		
		self.Tallene		= Tallene
		self.Navna			= Navna
		self.Typene			= Typene
		self.Korrekte_navn	= Korrekte_navn
		self.Antall			= len(Tallene)
	
	def _Print_oppsett(self, alt = False):
		"""
		Printer oppsettet for quizen, eller hele oppsettet med alle svarene hvis quizen skal avsluttes
		"""
		
		system("cls") # Sletter alt i terminalvinduet
		print("### QUIZ! ###")
		
		if alt: # Printer oppsett pluss svar hvis quizen skal avsluttes
			for i in range(len(self.Tallene)):
				if self.Hint == False:
					if self.Korrekte_navn[i] == self.Navna[i]:
						print("%03i V %s"%(self.Tallene[i], self.Navna[i]))
					else:
						print("%03i X %s "%(self.Tallene[i], self.Navna[i]))
				else:
					if self.Korrekte_navn[i] == self.Navna[i]:
						print("%03i V %-11s  %-8s %-8s"%(self.Tallene[i], self.Navna[i], self.Typene[i][0], self.Typene[i][1]))
					else:
						print("%03i X %-11s  %-8s %-8s"%(self.Tallene[i], self.Navna[i], self.Typene[i][0], self.Typene[i][1]))
		
		else: # Printer oppsett for quiz
			for i in range(len(self.Tallene)):
				if self.Hint == False:
					print("%03i  %s"%(self.Tallene[i], self.Korrekte_navn[i]))
				else:
					print("%03i  %-11s  %-8s %-8s"%(self.Tallene[i], self.Korrekte_navn[i], self.Typene[i][0], self.Typene[i][1]))
		
		# Printer antall korrekte svar funnet
		if self.Språk == 0: 
			print("Riktige svar: %i/%i"%(self.Korrekte, self.Antall))
		elif self.Språk == 1:
			print("Correct answers: %i/%i"%(self.Korrekte, self.Antall))
		else:
			print("# No language has been choosen. Ending quiz #")
			exit()
		
	def _Exit(self):
		"""
		Avslutter quizen ved å kalle på oppsett og printe tiden brukt
		"""
		
		self._Print_oppsett(alt = True) # Kaller på oppsett der svarene skal gis
		
		# Printer tiden
		if self.Språk == 0:
			print("# Avslutter quizen #")
			print("# Tid brukt er %i min og %i sek # "%((time() - self.start_tid) // 60, (time() - self.start_tid) % 60))
		elif self.Språk == 1:
			print("# Ending quiz #")
			print("# Time used is %i min and %i sec # "%((time() - self.start_tid) // 60, (time() - self.start_tid) % 60))
		else:
			print("# No language has been choosen. Ending quiz #")
			exit()
		
		exit() # Avslutter programmet

	def _Riktig_svar(self, Gitt):
		"""
		Oppdaterer lister hvis riktig svar er gitt, og printer nytt oppsett
		"""
		
		# Takler situasjonen der to pokemon har samme navn
		if Gitt == "Nidoran":
			self.Korrekte_navn[31] = Gitt
			self.Korrekte += 1
		
		# Oppdaterer lister
		self.Korrekte_navn[self.Navna.index(Gitt)] = Gitt
		self.Korrekte += 1
		
		self._Print_oppsett() # Printer nytt oppsett
	
	def Programmet(self):
		"""
		Selve programmet som kaller på funksjonene som skaffer språk, laster inn pokemon info, printer oppsett og starter timer.
		Tar imot svar og avgjør hva som skal gjøres med svaret utifra hva svaret er.
		"""
		self._Språk() # Bestemmer språk
		self._Skaff_Pokemon() # Laster pokemon info
		self._Print_oppsett() # Printer oppsett
		
		Navna		= self.Navna
		Antall		= self.Antall
		
		# Avgjør språk på beskjeder
		if self.Språk == 0: 
			input_tekst = "Pokemon [Skriv slutt for å avbryte quizen]: "
			slutt_tekst = ["Slutt", "slutt"]
			korr_navn_tekst = "Den pokemonen er allerede gitt."
			feil_tekst = "Feil navn eller stavemåte, prøv igjen!"
			ferdig_tekst = "# Gratulerer!!! Du klarte det #"
		elif self.Språk == 1:
			input_tekst = "Pokemon [Write quit to end quiz]: "
			slutt_tekst = ["Quit", "quit"]
			korr_navn_tekst = "This Pokemon has already been given."
			feil_tekst = "Wrong name or spelling. Please try again!"
			ferdig_tekst = "# Congratulations!!! You did it #"
		else:
			print("# No language has been choosen. Ending quiz #")
			exit()
		
		self._Start_Timer()	# Starter timer
		
		while self.Korrekte < Antall: # Selve løkka som slutter når alle svar er funnet eller bruker gir opp
			Gitt = input(input_tekst) # Tar imot input
			
			if Gitt in slutt_tekst: # Avslutter hvis bruker gir opp
				self._Exit()
			
			elif Gitt in ["Hint", "hint"]: # Fikser bruk av hint
				self.Hint = not self.Hint
				self._Print_oppsett()
			
			elif Gitt in self.Korrekte_navn: # Takler når korrekte svar blir gitt flere ganger
				print(korr_navn_tekst)

			elif Gitt in Navna: # Takler hvis svaret er riktig
				self._Riktig_svar(Gitt)
			
			else: # Takler hvis gitt svar ikke tilhører noen av de tidligere kategoriene
				print(feil_tekst)
		
		print(ferdig_tekst) # Printer hvis bruker klarte alle riktige svar
		self._Exit() # Avslutter quizen når den er ferdig.
	
if __name__ == "__main__":
	A = Quiz()
	A.Programmet()
