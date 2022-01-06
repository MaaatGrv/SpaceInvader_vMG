from tkinter import *
from tkinter import messagebox
from tkinter import filedialog

## Fonctions nécessaires au jeux ##

#Redémarrage du jeu
def refresh():
    fen1.destroy()
    fen1.__init__()

#Fonction permettant le mouvement du vaisseau avec la clavier
ListeBullet=[]

def Clavier(event):

    global PosX, PosY
    touche = event.keysym

    #déplacement vers la gauche et limitation aux bordures
    if touche == 'Left' and PosX > 15:
        PosX -=5

    #déplacement vers la droite et limitation aux bordures
    if touche == 'Right' and PosX < 907:
        PosX +=5

    if touche == 'space' :
        Shot(PosX)

    Canevas.coords(SpaceCadet, PosX -10, PosY -10, PosX +10, PosY +10)

def Shot(PosX):
    #Création et lancement de la balle
    global PosY, PosBulletY
    
    PosBulletX = PosX
    PosBulletY = 640

    Bullet = Canevas.create_oval(PosBulletX -2, PosBulletY -2, PosBulletX +2, PosBulletY +2, fill='green')

    ListeBullet.append([Bullet,PosBulletX,PosBulletY])

    print(ListeBullet)

## Affichage Tk ##

fen1 = Tk()
fen1.title('SpaceInvader')

#Mise en place du canevas
Largeur = 917
Hauteur = 688
Canevas = Canvas(fen1, width = Largeur, height = Hauteur, bg = 'white')

#Mise en place du Pion
PosX = 458
PosY = 640
SpaceCadet = Canevas.create_oval(PosX -10, PosY -10, PosX +10, PosY +10, width = 5, fill='red')

Canevas.focus_set()
Canevas.bind('<Key>', Clavier)

txt1 = Label(fen1,text = 'Score :')
txt2 = Label(fen1,text = 'Record :')
txt3 = Label(fen1,text = 'Vies :')

playButton = Button(fen1, text = 'Jouer')
tryAgainButton = Button(fen1, text = 'Recommencer', command = refresh)
quitButton = Button(fen1, text = 'Quitter', command = fen1.destroy)

txt1.grid(row =1, column =1, sticky ='ew')
txt2.grid(row =1, column =2, sticky ='ew')
txt3.grid(row =1, column =3, sticky ='ew')
Canevas.grid(row =2, column =1, columnspan =3, sticky='ew')
playButton.grid(row =3, column =1, sticky ='ew')
tryAgainButton.grid(row =3, column =2, sticky ='ew')
quitButton.grid(row =3, column =3, sticky ='ew')

fen1.mainloop()