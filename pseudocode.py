import sysv_ipc
from multiprocessing import Process, Manager
from threading import Lock

mutexPioche = Lock()
mutexQueue = Lock()


key =19
mq = sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREAT)

class Joueur:
	def __init__(self, identifiant, l, t):
		self.id=identifiant
		self.main= l
		self.timer= t
	def ajouterCarte (self,carte):
		self.main.append(carte)
class Carte:
	def __init__(self, val, couleur):
		self.couleur=couleur
		self.valeur = val
		
def piocher(j): #Permet à un joueur de piocher une carte
	
	a=int(random.random() * (len(pioche)))
	j.ajouterCarte(pioche[a])
	del pioche[a]

"""#def estFini(): #Cette fonction vérifie si l'un des deux joueurs n'a plus de carte ou si la pioche est vide.
	# Si oui, elle envoie un signal au thread principal qui tuera tous les autres thread et process et qui affichera le vainqueur. Cette fonction sera multithreadé
	
#def entreeClavier() : #Cette fonction vérifie les différentes entrées du clavier et envoie un signal aux process joueur concernés, indiquant quelle carte il devra jouer
	# Par exemple une touche correspondra a une carte d'un joueur, cette finction sera multithreadé
"""	
def jouer(carte,j) : #Place la carte dans le message queue, executé par les process joueurs
	message = str(j.identifiant) + ":" + str(carte.valeur) + ":" + str(carte.couleur)
	msg= str(message).encode()
	mutexQueue.acquire()
	mq.send(msg, type=1)
	m, t =mq.receive(type=1+j.identifiant)
	mutexQueue.release()
	valid = m.decode()
	if valid:
		j.main.remove(carte)
	else : 
		piocher(j)
		

	
def is_valid(carteActu): #Vérifie que la dernière carte de la queue est valide par rapport à la carte courante, qui sera une variable du board, si oui elle devient la carte courante, sinon 
	#le board envoie un signal qui informe le process du joueur qu'il doit récuperer la carte de la queue et en piocher une nouvelle, fonction executé par le board

	m, t = mq.receive(type=1)
	message =m.decode()
	message=message.split(":")
	identifiant=int(message[0])
	carte=Carte(int(message[1]), message[2])
	if (carte.couleur == carteActu.couleur and carte.valeur==carteActu.valeur + 1) or (carte.couleur == carteActu.couleur and carte.valeur==carteActu.valeur - 1) or (carte.valeur==carteActu.valeur):
		resultat = True
	else :
		resultat = False
	msg= str(resultat).encode()
	mq.send(msg, type=indentifiant+1)
	
	
		
"""	

def resetTimer(j) : #Réinitialise le timer d'un joueur, quand le joueur a joué ou que celui ci a atteint 0

def decTimer(j) : #Décrement le timer, cette fonction sera multithreader par un process joueur
"""	

if __name__ == "__main__":
	with Manager() as manager:
		
		pioche =manager.list()     #Création d'une liste partagée représentant la pioche 
		for i in range(10):
			pioche.append(Carte(i+1, "Rouge"))
			pioche.append(Carte(i+1, "Bleue"))
		
