###                          À FAIRE                         ###
#                                                              #
#   Trouver un moyen de faire les a/r des vaisseaux ennemis    #
#   Ajouter des vaisseaux ennemis                              #
#   Ajouter les tirs ennemis                                   #
#   Ajouter les vies du ship et des vilains                    #  
              

import tkinter as tk
 
SCREEN = 917, 688
         
class Bullet:
    def __init__(self, canvas, x, y, tk_fill, movement):
        self.bullet = canvas.create_oval(x -3 , y - 3, x + 3, y + 3, fill=tk_fill)
        self.movement = movement
         
    def move(self, canvas):
        canvas.move(self.bullet, self.movement[0], self.movement[1]) 

class Vilains:
    def __init__(self, canvas, x, y, tk_fill, movement):
        self.vilain = canvas.create_polygon(x, y + 60, x - 20, y + 30, x + 20, y + 30, fill=tk_fill)
        self.movement = movement

    def move_right(self, canvas):
        canvas.move(self.vilain, -self.movement[1], self.movement[0])

    def move_left(self, canvas):
        canvas.move(self.vilain, self.movement[1], self.movement[0])

class App(tk.Frame):
    def __init__(self, master):
        # put canvas in frame so you can have other goodies
        tk.Frame.__init__(self, master)
        self.canvas = tk.Canvas(self, width=SCREEN[0], height=SCREEN[1], bg = 'white')
        self.canvas.pack()
        self.bullets = [] # store bullets
        self.vilains = [] # store vilains
        self.tick_loop() # start the tick loop
        self.tick_loop_vilains()
        self.ship = self.create_ship(458, 640, "blue")
    
        master.bind("<Left>", self.go_left)
        master.bind("<Right>", self.go_right)
        master.bind("<space>", self.space_key)
        master.bind("<v>", self.go_v)
        master.bind("<a>", self.create_vilain)
    
    def create_ship(self, x, y, tk_fill):
        return self.canvas.create_polygon(x, y, x - 20, y + 30, x + 20, y + 30, fill=tk_fill)
         
    def tick_loop(self):
        remove_list = []
        for enum, bullet in enumerate(self.bullets):
            coords = self.canvas.coords(bullet.bullet)
            if coords[1] < 0 or coords[0] < 0 or coords[2] > SCREEN[0]:
                remove_list.append(enum)
                self.canvas.delete(bullet.bullet)
            else:
                bullet.move(self.canvas)
         
        # fix poping bug        
        for enum, index in enumerate(remove_list):
            self.bullets.pop(index - enum)
     
        # framerate per seconds 1000/30 = 30 frames roughly
        self.after(int(1000/30), self.tick_loop) 

    def tick_loop_vilains(self):
        remove_list = []
        data=[]
        for enum, vilain in enumerate(self.vilains):
            coords = self.canvas.coords(vilain.vilain)
            if coords[0] < 50 :
                vilain.move_left(self.canvas)
                data.append('l')
            
            if coords[0] > 900 :
                vilain.move_right(self.canvas)
                data.append('r')
                
            if coords[0] < 900 and coords[0] > 50:
                if data == []:
                    vilain.move_right(self.canvas)
                else :
                    if data[0] == 'l' :
                        vilain.move_left(self.canvas)
                    if data[0] == 'r' :
                        vilain.move_right(self.canvas)

         
        # fix poping bug        
        for enum, index in enumerate(remove_list):
            self.vilains.pop(index - enum)
     
        # framerate per seconds 1000/30 = 30 frames roughly
        self.after(int(1600/30), self.tick_loop_vilains) 

    def go_left(self, event):
        self.canvas.move(self.ship, -5, 0)
        self.canvas.update()
         
    def go_right(self, event):
        self.canvas.move(self.ship, 5, 0)
        self.canvas.update()
         
    def space_key(self, event=0):
        # only want the first two coords
        x, y = self.canvas.coords(self.ship)[:2]
        # just having shoot straight up
        self.bullets.append(Bullet(self.canvas, x, y, "blue", (0, -10)))
    
    # triple shoot striaght up
    def go_v(self, event):
        # only want the first two coords
        x, y = self.canvas.coords(self.ship)[:2]        
        #up
        self.bullets.append(Bullet(self.canvas, x, y, "green", (0, -5)))
        self.bullets.append(Bullet(self.canvas, x - 50, y, "green", (0, -5)))
        self.bullets.append(Bullet(self.canvas, x + 50, y, "green", (0, -5)))
    
    def create_vilain(self,event):
        # only want the first two coords
        x, y = self.canvas.coords(self.ship)[:2]
        # just having shoot straight up
        self.vilains.append(Vilains(self.canvas, x, 10, "red", (0, +10)))


def main():
    root = tk.Tk()
    app = App(root)

    root.title('SpaceInvader')

    txt1 = tk.Label(root,text = 'Score :')
    txt2 = tk.Label(root,text = 'Record :')
    txt3 = tk.Label(root,text = 'Vies :')

    playButton = tk.Button(root, text = 'Jouer')
    tryAgainButton = tk.Button(root, text = 'Recommencer')
    quitButton = tk.Button(root, text = 'Quitter', command = root.destroy)

    txt1.grid(row =1, column =1, sticky ='ew')
    txt2.grid(row =1, column =2, sticky ='ew')
    txt3.grid(row =1, column =3, sticky ='ew')
    app.grid(row =2, column =1, columnspan =3, sticky='ew')
    playButton.grid(row =3, column =1, sticky ='ew')
    tryAgainButton.grid(row =3, column =2, sticky ='ew')
    quitButton.grid(row =3, column =3, sticky ='ew')
    
    app.mainloop()
     
if __name__ == '__main__':
    main()