import random
import multiprocessing
import threading
from multiprocessing import Process, Manager
import sysv_ipc

mutexPioche = multiprocessing.Lock()
mutexQueue = multiprocessing.Lock()

class Joueur:
	def __init__(self, id, l):
		self.id=id
		self.main= l 
	def ajouterCarte (self,carte):
		self.main.append(carte)
class Carte:
	def __init__(self, val, couleur):
		self.couleur=couleur
		self.valeur = val
		
#key = 12
#pile = sysv_ipc.MessageQueue(key)




def piocher(j):
	
	a=int(random.random() * (len(pioche)))
	j.ajouterCarte(pioche[a])
	del pioche[a]
	
	

	
	
def jouer(j,n):
	for i in range(n):
		mutexPioche.acquire()
		piocher(j)
		mutexPioche.release()


	

if __name__ == "__main__":
	with Manager() as manager:
		
		pioche =manager.list()
		l1=manager.list()
		l2=manager.list()
		for i in range(10):
			pioche.append(Carte(i+1, "Rouge"))
			pioche.append(Carte(i+1, "Bleue"))
		j1 = Joueur(1,l1)
		j2 = Joueur(2,l2)
		p1 = Process(target=jouer, args=(j1,5))
		p2 = Process(target=jouer, args=(j2,5))
		p1.start()
		p2.start()
		p2.join()
		p1.join()
		print("**********J1*******")
		for i in range (len(j1.main)):
			print(j1.main[i].valeur, j1.main[i].couleur)
		print("**********J2*******")
		for i in range (len(j2.main)):
			print(j2.main[i].valeur, j2.main[i].couleur)
		print("**********PAQUET*******")
		for i in range (len(pioche)):
			print(pioche[i].valeur, pioche[i].couleur)
