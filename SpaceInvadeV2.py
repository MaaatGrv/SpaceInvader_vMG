###             À FAIRE                           ###
#                                                   #
#   Affichage de Game Over et Victoire              #

"""
Author : Mathis Gorvien (@MatGrv)
Date : January 2022

SpaceInvader vMG (School Project)

Il est possible d'ajouter des niveaux si l'on veut à partir de la ligne 45
/!\ Certains ennemis peuvent avoir plusieurs points de vies cependant ils ont la même apparence :)
"""       

from tkinter import *
from random import *
import copy

def main(): #Exécution du programme
    class Game():
        def __init__(self, MainWindow):
            self.level=1
            #Déclaration des différents types d'ennemis
            self.Vilain1={'Vies' : 1, 'Vitesse':1, 'Points' : 10, 'CadenceTir' : 5000}
            self.Vilain2={'Vies' : 2, 'Vitesse':2, 'Points' : 20, 'CadenceTir' : 4000}
            self.Vilain3={'Vies' : 2, 'Vitesse':3, 'Points' : 30, 'CadenceTir' : 3000}
            self.score=0
            self.nbMissile=0 #Limitation du nombre de missiles
            self.Vilain=[] #Liste des ennemis actifs
            self.vies=3
            self.Shots=[] #Liste des laser actifs
            self.MainWindow=MainWindow
        


        def environement(self):
            self.step() #Fonction qui gère le choix du niveau une fois que tous les ennemis sont éliminés
            self.DisplayScore = Label(self.MainWindow, text='Score: '+str(self.score))
            self.DisplayScore.pack(padx=3, pady=3, anchor=E)
            self.DisplayVies = Label(self.MainWindow, text='Vies: '+str(self.vies))
            self.DisplayVies.pack(padx=3, pady=3, anchor=W)
            self.DisplayNiveau = Label(self.MainWindow, text='Niveau: '+str(self.level))
            self.DisplayNiveau.pack(padx=3, pady=3, anchor=N)

            self.Block=[] #Génération de l'ilot centale
            for j in [10,30,50]: 
                for i in [10,30,50,70,90]:
                    self.Block.append(GameCanvas.create_rectangle( i+180, 300+j,i+200, 320+j, fill= 'chocolate1'))
        
        def step(self):
            if self.level == 1:
                GameCanvas.after(10, self.CreateVilain, GameCanvas, self.Vilain1)
            
            elif self.level == 2:
                GameCanvas.after(10, self.CreateVilain, GameCanvas, self.Vilain1)
                GameCanvas.after(1200, self.CreateVilain, GameCanvas, self.Vilain1)
            
            elif self.level == 3:
                GameCanvas.after(10, self.CreateVilain, GameCanvas, self.Vilain1)
                GameCanvas.after(10, self.CreateVilain, GameCanvas, self.Vilain2)
                GameCanvas.after(1200, self.CreateVilain, GameCanvas, self.Vilain2)
            
            elif self.level == 4:
                GameCanvas.after(10, self.CreateVilain, GameCanvas, self.Vilain1)
                GameCanvas.after(10, self.CreateVilain, GameCanvas, self.Vilain2)
                GameCanvas.after(1200, self.CreateVilain, GameCanvas, self.Vilain2)
                GameCanvas.after(70, self.CreateVilain, GameCanvas, self.Vilain3)
                
            elif self.level == 5:
                GameCanvas.after(10, self.CreateVilain, GameCanvas, self.Vilain1)
                GameCanvas.after(1200, self.CreateVilain, GameCanvas, self.Vilain2)
                GameCanvas.after(2200, self.CreateVilain, GameCanvas, self.Vilain3)
                GameCanvas.after(3200, self.CreateVilain, GameCanvas, self.Vilain3)
                GameCanvas.after(4200, self.CreateVilain, GameCanvas, self.Vilain3)

        def CreateVilain(self, GameCanvas, Vilain): 
            VilainPic1 = PhotoImage(file='vilain.gif')
            label = Label(image=VilainPic1)
            label.image=VilainPic1
            Vilain['largeur']=VilainPic1.width() #Récupère les dimensions de l'image pour générer la hitbox
            Vilain['hauteur']=VilainPic1.height()
            Vilain1 = GameCanvas.create_image(250,40, anchor=CENTER, image=VilainPic1)
            self.Vilain.append(Vilain1) #Ajout à la liste des ennemis
            DescVilain = copy.deepcopy(Vilain) #Caractéristiques de l'ennemi sont saved
            GameCanvas.after(1000, self.down, GameCanvas, Vilain1, DescVilain)
            self.update(GameCanvas, Vilain1, 0, DescVilain)
            GameCanvas.after(100, self.VilainShots, GameCanvas, Vilain1, DescVilain)
        
        def down(self, GameCanvas, Vilain, DescVilain):
            try:
                if GameCanvas.coords(Vilain)[1]>500:
                    GameCanvas.delete(Vilain)

                if GameCanvas.coords(Vilain)[0]<50 or GameCanvas.coords(Vilain)[0]>450: #Les ennemis baissent quand ils touchent les bords
                    GameCanvas.move(Vilain, 0, DescVilain["Vitesse"])
                GameCanvas.after(500, self.down, GameCanvas, Vilain, DescVilain)
            except:
                Vilain=None

        def VilainShots(self, GameCanvas, Vilain, DescVilain):
            try:
                RandomShot = randrange(DescVilain['CadenceTir']-300, DescVilain['CadenceTir']+300) #Les tirs sont créés de manière aléatoire
                Bullet = GameCanvas.create_rectangle(GameCanvas.coords(Vilain)[0]+2,GameCanvas.coords(Vilain)[1],GameCanvas.coords(Vilain)[0]-2,GameCanvas.coords(Vilain)[1]+15, fill= 'blue')
                self.updateVilainShot(GameCanvas,Bullet,DescVilain)
                GameCanvas.after(RandomShot, self.VilainShots, GameCanvas, Vilain, DescVilain)
            except:
                Vilain=None

        def updateVilainShot(self, GameCanvas, Bullet, DescVilain):

            GameCanvas.move(Bullet, 0, DescVilain['Vitesse'])

            try:
                touche=GameCanvas.find_overlapping(GameCanvas.coords(Bullet)[0],GameCanvas.coords(Bullet)[1],GameCanvas.coords(Bullet)[2],GameCanvas.coords(Bullet)[3])#test les chevauchements avec d autres objets
                for i in touche:
                    if i in self.Block: #Suppression des blocs si touchés par les tirs ennemis
                        GameCanvas.delete(i)
                        GameCanvas.delete(Bullet)
                    
                    if i == 2 :
                        self.vies -= 1 #Si le vaisseau est touché, il perd une vie
                        self.DisplayVies.config(text='Vies: '+str(self.vies))
                        if self.vies == 0: #Game Over quand il n'y a plus de vies
                            self.MainWindow.destroy()

                        GameCanvas.delete(Bullet)
            except:
                Bullet=None

            try:
                if GameCanvas.coords(Bullet)[1]>510: #Les tirs sont supprimés si ils sortent de l'écran
                            GameCanvas.delete(Bullet)
                else:
                    GameCanvas.after(5, self.updateVilainShot, GameCanvas , Bullet,DescVilain)
            except: 
                Bullet=None

        
        def update(self, GameCanvas, Vilain, n, DescVilain):
            GameCanvas.bind_all('<space>', lambda event : self.Shot(GameCanvas, Vilain)) #Tirs lorsque la touche espace est pressée
            try:
                touche=GameCanvas.find_overlapping(GameCanvas.coords(Vilain)[0]-DescVilain['largeur']/2,GameCanvas.coords(Vilain)[1]-DescVilain['hauteur']/2,GameCanvas.coords(Vilain)[0]+DescVilain['largeur']/2,GameCanvas.coords(Vilain)[1]+DescVilain['hauteur']/2)#test le chevauchement avec un autre objet
                for i in touche:
                    if i in self.Block :
                        GameCanvas.delete(i)
                    if i in self.Shots: 
                        GameCanvas.delete(i) #Les missiles sont supprimés quand ils touchent un vaiseau
                        self.Shots.remove(i)
                        
                        DescVilain['Vies']=DescVilain['Vies']-1
                        if DescVilain['Vies']==0:
                            GameCanvas.delete(Vilain)
                            self.Vilain.remove(Vilain)
                            self.score+=DescVilain["Points"]
                            self.DisplayScore.config(text='Score: '+str(self.score))

                    if i==2: #L'élément 2 correspond au vaisseau (Ship)
                        self.vies -= 1
                        self.DisplayVies.config(text='Vies: '+str(self.vies))
                        if self.vies==0 :
                            GameCanvas.delete(Ship)
                                
                        GameCanvas.delete(Vilain)
                        self.Vilain.remove(Vilain)
                        self.score+=DescVilain["Points"]
                        self.DisplayScore.config(text='Score: '+str(self.score))

            except:
                Vilain=None

            try:
                if (GameCanvas.coords(Vilain)[1]) >=510:
                    GameCanvas.delete(Vilain)
                    self.Vilain.remove(Vilain)   

                if (GameCanvas.coords(Vilain)[0] <=14) or (GameCanvas.coords(Vilain)[0] >=486)  : #Le vaisseau se déplace si il n'y a pas de collison
                    n+=1
        
                GameCanvas.move(Vilain,DescVilain["Vitesse"]*(-1)**n,0)
                GameCanvas.after(18, self.update, GameCanvas,Vilain,n,DescVilain)

            except : 
                Vilain = None
            if self.Vilain==[]: #Le niveau est terminé quand tous les ennemis du niveau sont éliminés
                self.level+=1
                self.DisplayNiveau.config(text='Niveau: '+str(self.level))
                self.step()

        
        def go_right(self, event):
            try :
                if GameCanvas.coords(Ship)[0] < 500:
                    GameCanvas.move(Ship, 7,0)
            except:
                GameCanvas.Ship=None
        
        def go_left(self, event):
            try:
                if GameCanvas.coords(Ship)[0] > 15:
                    GameCanvas.move(Ship, -7,0)
            except:
                GameCanvas.Ship=None

        def Shot(self, GameCanvas,Vilain):
            if self.nbMissile == 0:
                Bullet = GameCanvas.create_rectangle(GameCanvas.coords(Ship)[0]-2,GameCanvas.coords(Ship)[1]-40,GameCanvas.coords(Ship)[0]+2,GameCanvas.coords(Ship)[1]- 20, fill= 'red')
                self.nbMissile=1
                self.Shots.append(Bullet)
                self.updateBullet(GameCanvas, Vilain, Bullet)
                GameCanvas.after(600, self.Latence) #Permet d'éviter le spam de tirs sans quoi le jeu est trop facile

        def Latence(self):
            self.nbMissile=0
        
        def updateBullet(self, GameCanvas, Vilain, Bullet):
            try: #Test de collision avec les blocs
                touche=GameCanvas.find_overlapping(GameCanvas.coords(Bullet)[0],GameCanvas.coords(Bullet)[1],GameCanvas.coords(Bullet)[2],GameCanvas.coords(Bullet)[3])
                for i in touche:
                    if i in self.Block:
                        GameCanvas.delete(i)
                        GameCanvas.delete(Bullet)
            except:
                Bullet=None

            try:
                GameCanvas.move(Bullet,0,-5)
                if GameCanvas.coords(Bullet)[1]<0:       
                    GameCanvas.delete(Bullet)
                else:
                    GameCanvas.after(5, self.updateBullet, GameCanvas,Vilain,Bullet) 
            except:
                Bullet=None

    #Gestion des fenêtres
    MainWindow = Tk()    
    Game1=Game(MainWindow)
    MainWindow.title('SpaceInvader')
        
    PlayButton=  Button (MainWindow, text='Démarrer' ,command= Game1.environement)
    PlayButton.pack (padx=3,  pady= 3)
    
    QuitButton = Button (MainWindow, text='Quitter', command= MainWindow.destroy)
    QuitButton.pack (padx=3,  pady= 3)
    
    GameCanvas = Canvas(MainWindow, height = 500, width = 500 , bg='black')
    GameCanvas.pack (padx=3,  pady= 3)
    Background = PhotoImage(file='space_bg.gif')
    GameCanvas.create_image(250,250, anchor=CENTER ,image=Background)
    Ship1 = PhotoImage(file='spaceship.gif')
    Ship1 = Ship1.subsample(2,2)
    Ship = GameCanvas.create_image(250, 450 , anchor=CENTER ,image=Ship1)
    
    GameCanvas.bind_all("<Right>", Game1.go_right)
    GameCanvas.bind_all("<Left>", Game1.go_left)
        
    MainWindow.mainloop()

main()