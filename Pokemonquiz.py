""" Pokemon quiz """

from sys import exit
from os import system
from time import time

class Quiz():
	def __init__(self):
		self.Hint		= False
		self.Korrekte	= 0
		self.Alle_regioner = ["Kanto", "Johto", "Hoenn", "Sinnoh"]
		self.Avslutt = ["Avslutt", "avslutt", "Slutt", "slutt"]
	
	def _Meny(self):
		Oppsett = ["###########################", "#                         #", "#                         #", "#       Pokemonquiz       #", "#                         #", "#                         #",\
		"#  Av Torstein S Oelberg  #", "#                         #", "# Tilgjengelige regioner: #", "#          Kanto          #", "#          Johto          #", "#          Hoenn          #", "#          Sinnoh         #",\
		"#                         #", "#                         #", "###########################"]
		
		system("cls")
		for line in Oppsett:
			print(line)


	def _Region(self):
		Region = input("Hvilke(n) Region(er)? ").split()
		
		bindeord = ["and", "And", "og", "Og"]
		indekser = []
		
		for i in range(len(Region)):
			if Region[i] in bindeord:
				indekser.append(i)
			elif Region[i][-1] == ",":
				Region[i] = Region[i][:-1]
		for i in indekser:
			Region.pop(i)
		
		for i in range(len(Region)):
			while Region[i] not in self.Alle_regioner:
				if Region[i] in ["Alle", "alle"]:
					Region = self.Alle_regioner
				elif Region[i] in self.Avslutt:
					print("Avslutter program.")
					exit()
				else:
					print("Regionen %s eksisterer ikke, eller er for ny. Velg en annen."%Region[i])
					Region[i] = input("Hvilke(n) Region(er)? ").split()[0]
		
		self.Region = Region
	
	def _Start_Timer(self):
		self.start_tid = time()
	
	def _Skaff_Pokemon(self):
		with open("Pokedex.txt", "r") as innfil:
			Tallene			= []
			Navna 			= []
			Typene 			= []
			Korrekte_navn	= []
			
			self._Region()
			
			for i in range(2):
				innfil.readline()
			
			for linje in innfil:
				if len(linje.split()) <= 1:
					False
				elif linje.split()[1] in self.Alle_regioner:
					midl = linje.split()[1]
				
				elif linje.split()[1] not in self.Alle_regioner and midl in self.Region:
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
		system("cls")
		print("### QUIZ! ###")
		
		if alt == True:
			for i in range(len(self.Tallene)):
				if self.Hint == False:
					if self.Korrekte_navn[i] == self.Navna[i]:
						print("%03i   %s"%(self.Tallene[i], self.Navna[i]))
					else:
						print("%03i X %s "%(self.Tallene[i], self.Navna[i]))
				else:
					if self.Korrekte_navn[i] == self.Navna[i]:
						print("%03i   %-11s  %-8s %-8s"%(self.Tallene[i], self.Navna[i], self.Typene[i][0], self.Typene[i][1]))
					else:
						print("%03i X %-11s  %-8s %-8s"%(self.Tallene[i], self.Navna[i], self.Typene[i][0], self.Typene[i][1]))
		
		else:
			for i in range(len(self.Tallene)):
				if self.Hint == False:
					print("%03i  %s"%(self.Tallene[i], self.Korrekte_navn[i]))
				else:
					print("%03i  %-11s  %-8s %-8s"%(self.Tallene[i], self.Korrekte_navn[i], self.Typene[i][0], self.Typene[i][1]))
		
		print("Riktige svar: %i/%i"%(self.Korrekte, self.Antall))
	
	def _Exit(self):
		self._Print_oppsett(alt = True)
		print("# Avslutter quizen #")
		print("# Tid brukt er %i min og %i sek # "%((time() - self.start_tid) // 60, (time() - self.start_tid) % 60))
		exit()

	def _Riktig_svar(self, Gitt):
		Navna		= self.Navna
		
		if Gitt == "Nidoran":
			self.Korrekte_navn[31] = Gitt
			self.Korrekte += 1
				
		self.Korrekte_navn[Navna.index(Gitt)] = Gitt
		self.Korrekte += 1
		self._Print_oppsett()
	
	def _Programmet(self):
		self._Meny()
		self._Skaff_Pokemon()
		self._Print_oppsett()
		
		Navna		= self.Navna
		Antall		= self.Antall
		
		A._Start_Timer()
		
		while self.Korrekte < Antall:
			Gitt = input("Pokemon [Skriv Slutt for å avbryte quizen]: ")
			
			if Gitt in self.Avslutt:
				self._Exit()
			
			elif Gitt == "Hint" or Gitt == "hint":
				if self.Hint == False:
					self.Hint = True
				elif self.Hint == True:
					self.Hint = False
				self._Print_oppsett()
			
			elif Gitt in self.Korrekte_navn:
				print("Den pokemonen er allerede gitt")

			elif Gitt in Navna:
				self._Riktig_svar(Gitt)
			
			else:
				print("Feil navn eller stavemåte, prøv igjen!")
		
		print("# Gratulerer!!! Du klarte det #")
		print(" # Tid brukt er %.2f min # "%((time() - self.start_tid) / 60))
	
if __name__ == "__main__":
	A = Quiz()
	A._Programmet()