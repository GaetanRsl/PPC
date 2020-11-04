import sysv_ipc
from multiprocessing import Process, Manager, Value
import multiprocessing
import threading
from threading import Thread,Timer
import pygame
from pygame.locals import *
import random
import multitimer
import sys 
mutexPioche = multiprocessing.Lock()
mutexQueue = multiprocessing.Lock()
mutexAffichage=multiprocessing.Lock()

white = (255, 255, 255) 
black= (0, 0,0) 
X=1920
Y=1080


pygame.init() 

font = pygame.font.Font('freesansbold.ttf', 50)



fenetre = pygame.display.set_mode((X, Y), RESIZABLE)
fond = pygame.image.load("fondnoir.jpg").convert()
fenetre.blit(fond,(0,0))
pygame.display.flip()


pygame.mixer.music.load("theme.wav")
pygame.mixer.music.play()

son = pygame.mixer.Sound("son.wav")



key =int(random.random()*1000)
cle = key +1 
mq = sysv_ipc.MessageQueue(key, sysv_ipc.IPC_CREAT)
aff = sysv_ipc.MessageQueue(cle, sysv_ipc.IPC_CREAT)


class Joueur:
	def __init__(self, identifiant, l):
		self.identifiant=identifiant
		self.main= l
	def ajouterCarte (self,carte):
		self.main.append(carte)
class Carte:
	def __init__(self, val, couleur):
		self.couleur=couleur
		self.valeur = val
		
def piocher(j): #Permet à un joueur de piocher une carte
	if(len(pioche)!=0):
		if(len(j.main)<9):
			mutexPioche.acquire()
			son.play()
			a=int(random.random() * (len(pioche)))
			j.ajouterCarte(pioche[a])
			del pioche[a]
			mutexPioche.release()
			afficherMain(j)
			
	else : 
		message= "3" 
		message=message.encode()
		mq.send(message, type=4)

	
		
	
	
	
def entreeClavier() : 
	a=1
	#Cette fonction vérifie les différentes entrées du clavier et envoie un signal aux process joueur concernés, indiquant quelle carte il devra jouer
	#Par exemple une touche correspondra a une carte d'un joueur, cette finction sera multithreadé
	while a ==1:
		for event in pygame.event.get():   
			if event.type == KEYDOWN and event.key == K_a:
				message="0"
				message=message.encode()
				mq.send(message, type=5)
			if event.type == KEYDOWN and event.key == K_z:
				message="1"
				message=message.encode()
				mq.send(message, type=5)
			if event.type == KEYDOWN and event.key == K_e:
				message="2"
				message=message.encode()
				mq.send(message, type=5)
			if event.type == KEYDOWN and event.key == K_r:
				message="3"
				message=message.encode()
				mq.send(message, type=5)
			if event.type == KEYDOWN and event.key == K_t:
				message="4"
				message=message.encode()
				mq.send(message, type=5)
			if event.type == KEYDOWN and event.key == K_y:
				message="5"
				message=message.encode()
				mq.send(message, type=5)
			if event.type == KEYDOWN and event.key == K_u:
				message="6"
				message=message.encode()
				mq.send(message, type=5)
			if event.type == KEYDOWN and event.key == K_i:
				message="7"
				message=message.encode()
				mq.send(message, type=5)
			if event.type == KEYDOWN and event.key == K_o:
				message="8"
				message=message.encode()
				mq.send(message, type=5)
			if event.type == KEYDOWN and event.key == K_p:
				message="9"
				message=message.encode()
				mq.send(message, type=5)
			if event.type == KEYDOWN and event.key == K_w:
				message="0"
				message=message.encode()
				mq.send(message, type=6)
			if event.type == KEYDOWN and event.key == K_x:
				message="1"
				message=message.encode()
				mq.send(message, type=6)
			if event.type == KEYDOWN and event.key == K_c:
				message="2"
				message=message.encode()
				mq.send(message, type=6)
			if event.type == KEYDOWN and event.key == K_v:
				message="3"
				message=message.encode()
				mq.send(message, type=6)
			if event.type == KEYDOWN and event.key == K_b:
				message="4"
				message=message.encode()
				mq.send(message, type=6)
			if event.type == KEYDOWN and event.key == K_n:
				message="5"
				message=message.encode()
				mq.send(message, type=6)
			if event.type == KEYDOWN and event.key == K_COMMA:
				message="6"
				message=message.encode()
				mq.send(message, type=6)
			if event.type == KEYDOWN and event.key == K_SEMICOLON:
				message="7"
				message=message.encode()
				mq.send(message, type=6)
			if event.type == KEYDOWN and event.key == K_COLON:
				message="8"
				message=message.encode()
				mq.send(message, type=6)
			if event.type == KEYDOWN and event.key == K_EXCLAIM:
				message="9"
				message=message.encode()
				mq.send(message, type=6)
			if event.type == QUIT :
				a=0
				s=""
				s=s.encode()
				pygame.quit()
				sys.exit()
				
			
	

def jouer(j) : 	
	z= multitimer.MultiTimer(interval =10, function=piocher, kwargs = {"j":j}, runonstart=False)
	z.start()
	m, t=mq.receive(type=4 +j.identifiant)
	z.stop()
	numero = int(m.decode())
	if numero<len(j.main):
		carte=j.main[numero]
		message = str(j.identifiant) + ":" + str(carte.valeur) + ":" + str(carte.couleur)
		msg= str(message).encode()
		mutexQueue.acquire()
		mq.send(msg, type=1)
		m, t =mq.receive(type= 1+j.identifiant)
		mutexQueue.release()
		b = int(m.decode())
		if b==1:
			j.main.remove(carte)
		else : 
			piocher(j)
	if (len(j.main)==0):
			msg = str(j.identifiant)
			msg=msg.encode()
			mq.send(msg, type=4)
	afficherMain(j)
		

	
def is_valid(): #Vérifie que la dernière carte de la queue est valide par rapport à la carte courante, qui sera une variable du board, si oui elle devient la carte courante, sinon 
	#le board envoie un signal qui informe le process du joueur qu'il doit récuperer la carte de la queue et en piocher une nouvelle, fonction executé par le board
	a=1
	mutexPioche.acquire()
	b=int(random.random() * (len(pioche)))
	carteActu=pioche[b]
	del pioche[b]
	mutexPioche.release()
	
	
	
	
	while a ==1:
		mutexAffichage.acquire()
		x=str(carteActu.valeur)
		image=x + ":" + carteActu.couleur + ":" + "8"
		image=image.encode()
		aff.send(image, type=3)
		mutexAffichage.release()
		resultat=0
		m, t = mq.receive(type=1)
		message =m.decode()
		message=message.split(":")
		identifiant=int(message[0])
		carte=Carte(int(message[1]), message[2])
		if (carte.couleur == carteActu.couleur and carte.valeur%10==(carteActu.valeur+1)%10) or (carte.couleur == carteActu.couleur and carte.valeur%10==(carteActu.valeur-1)%10) or (carte.valeur==carteActu.valeur):
			resultat = 1
			carteActu=Carte(carte.valeur, carte.couleur)
			
		msg= str(resultat).encode()
		mq.send(msg, type=identifiant+1)
		
		
def afficherMain(j):
	message = " "
	message=message.encode()
	aff.send(message, type = 3 +j.identifiant)
	for i in range(len(j.main)):
		message =str(j.main[i].valeur) + ":" + str(j.main[i].couleur) + ":"+ str(i)
		message=message.encode()
		mutexAffichage.acquire()
		aff.send(message, type=j.identifiant)
		mutexAffichage.release()
				
def afficher():
	a=1
	while a==1:
		m,t= aff.receive()
		message= m.decode()
		message=message.split(":")
		if t==1:
			image= message[0] + " " + message[1] + ".png"
			uno = pygame.image.load(image).convert()
			i=int(message[2])
			fenetre.blit(uno,(205*i,0))
			pygame.display.update()
		if t==2:
			image= message[0] + " " + message[1] + ".png"
			uno = pygame.image.load(image).convert()
			i=int(message[2])
			fenetre.blit(uno,(205*i,900))
			pygame.display.update()
		if t==3:
			son.play()
			image= message[0] + " " + message[1] + ".png"
			uno = pygame.image.load(image).convert()
			i=int(message[2])
			fenetre.blit(uno,(800,450))
			
			pygame.display.update()
		if t==4 : 
			image = "fondnoirbas.jpg"
			uno = pygame.image.load(image).convert()
			fenetre.blit(uno,(0,0))
			pygame.display.update()
		if t==5: 
			image = "fondnoirbas.jpg"
			uno = pygame.image.load(image).convert()
			fenetre.blit(uno,(0,880))
			pygame.display.update()
		if t==6:
			a=0
		if t==7:
			a=0
			msg=""
			msg=msg.encode()
			mq.send(msg, type=10)
			mq.send(msg, type=11)
			mq.send(msg, type=12)
	
	
		
		
		
def fgamer(j):
	a = 1
	for i in range(5):
		piocher(j)
		afficherMain(j)
	
		
	while a==1 :
		try:
			m, t = mq.receive(block=False, type=9+j.identifiant)
			if t==9+j.identifiant:
				a=0
			break 
		except sysv_ipc.BusyError:
			print("")
		jouer(j)
	
		
def finPartie():
	m,t =mq.receive(type=4)
	m=m.decode()
	n=int(m)
	if(t==4):
		print("Fin de Partie!")
		msg=""
		msg=msg.encode()
		aff.send(msg, type=6)
		mq.send(msg, type=10)
		mq.send(msg, type=11)
		mq.send(msg, type=12) 
	if n==3:
		message="Partie terminée! Ex-aequo !"
	else:
		message = "Le joueur " + m + " a gagné ! "
	text = font.render(message, True, white, black)
	textRect = text.get_rect() 
	textRect.center = (X // 2, Y // 2) 
	while True : 
		fenetre.fill(black) 
		fenetre.blit(text, textRect)  
		for event in pygame.event.get() : 
			if event.type == pygame.QUIT : 
				pygame.quit() 
				sys.exit() 
			pygame.display.update() 
			
	
		

		

if __name__ == "__main__":
	with Manager() as manager:
		
		pioche =manager.list()    #Création d'une liste partagée représentant la pioche 
		for i in range(10):
			pioche.append(Carte(i, "Rouge"))
			pioche.append(Carte(i, "Bleue"))
		for i in range(18):
			if i<=8:
				image= str(i) + ".png"
				uno = pygame.image.load(image).convert()
				fenetre.blit(uno,(90+205*i,350))
				
			else:
				image= str(i) + ".png"
				uno = pygame.image.load(image).convert()
				fenetre.blit(uno,(90+205*(i-9),800))
		pygame.display.update()
				
		j1= Joueur(1,[])
		p1= Process(target=fgamer, args=(j1,))
		j2= Joueur(2,[])
		t = Thread(target=afficher, args=())
		t2 = Thread(target=finPartie, args=())
		p2= Process(target=fgamer, args=(j2,))
		t3=Thread(target=entreeClavier,args=())
		t4= Thread(target=is_valid, args=())
		p1.start()
		t.start()
		t2.start()
		p2.start()
		t3.start()
		t4.start()
		t3.join()
		t.join()
		t2.join()
		p1.join()
		p2.join()
		t4.join()
		
		
		
		
		
		
			
			
