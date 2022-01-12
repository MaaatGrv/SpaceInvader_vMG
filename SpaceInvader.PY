###                          À FAIRE                         ###
#                                                              #
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

class Bullet2:
    def __init__(self, canvas, x, y, tk_fill, movement):
        self.bullet2 = canvas.create_oval(x -3 , y - 3, x + 3, y + 3, fill=tk_fill)
        self.movement = movement

    def move(self, canvas):
        canvas.move(self.bullet2, self.movement[0], self.movement[1]) 

class Vilains:
    def __init__(self, canvas, x, y, tk_fill, movement):
        self.vilain = canvas.create_polygon(x, y + 60, x - 20, y + 30, x + 20, y + 30, fill=tk_fill)
        self.movement = movement
    def move_right(self, canvas):
        canvas.move(self.vilain, self.movement[1], self.movement[0])

    def move_left(self, canvas):
        canvas.move(self.vilain, -self.movement[1], self.movement[0])

    def move_down(self, canvas):
        canvas.move(self.vilain, self.movement[0], 50)
class App(tk.Frame):
    def __init__(self, master):
        # put canvas in frame so you can have other goodies
        tk.Frame.__init__(self, master)
        self.canvas = tk.Canvas(self, width=SCREEN[0], height=SCREEN[1], bg = 'white')
        self.canvas.pack()
        self.bullets = [] # store bullets
        self.bullets2 = [] # store bullets
        self.vilains = [] # store vilains
        self.vil_dir = 0 # store direction
        self.vil_step = 0 # store level in term of direction
        self.tick_loop() # start the tick loop
        self.tick_loop_vilains()
        self.ship = self.create_ship(458, 640, "blue")
        self.vies = 3

        #Keyboards events
        master.bind("<Left>", self.go_left)
        master.bind("<Right>", self.go_right)
        master.bind("<space>", self.space_key)
        master.bind("<v>", self.go_v)
        master.bind("<a>", self.create_vilain)
        master.bind("<b>", self.Lot_of_shots)
    
    def create_ship(self, x, y, tk_fill):
        return self.canvas.create_polygon(x, y, x - 20, y + 30, x + 20, y + 30, fill=tk_fill)

    def create_vilain(self,event):
        x, y = self.canvas.coords(self.ship)[:2]
        return self.vilains.append(Vilains(self.canvas, x, 10, "red", (0, +10)))
         
    def tick_loop(self):
        remove_list = []
        remove_list2 = []
        for enum, bullet in enumerate(self.bullets):
            coords = self.canvas.coords(bullet.bullet)
            if coords[1] < 0 or coords[0] < 0 or coords[2] > SCREEN[0]:
                remove_list.append(enum)
                self.canvas.delete(bullet.bullet)
            else:
                bullet.move(self.canvas)
        for enum, bullet2 in enumerate(self.bullets2):
            coords = self.canvas.coords(bullet2.bullet2)
            if coords[1] < 0 or coords[0] < 0 or coords[2] > SCREEN[0]:
                remove_list2.append(enum)
                self.canvas.delete(bullet2.bullet2)
            else:
                bullet2.move(self.canvas)
        # fix poping bug        
        for enum, index in enumerate(remove_list):
            self.bullets.pop(index - enum)
        for enum, index in enumerate(remove_list2):
            self.bullets2.pop(index - enum)
        # framerate per seconds 1000/30 = 30 frames roughly
        self.after(int(1000/30), self.tick_loop) 

    #Switch direction function that make vilains go down when the block arrive to limits
    def tick_loop_vilains(self):
        # 0 : to the left
        # 1 : to the right
        remove_list = []
        for enum, vilain in enumerate(self.vilains):
            coords = self.canvas.coords(vilain.vilain)
            dir = self.vil_dir
            if coords[0] < 30 :
                for enum2, vilain2 in enumerate(self.vilains):
                    vilain2.move_down(self.canvas)
                    vilain2.move_right(self.canvas)
                self.vil_dir = 1 
         
            if coords[0] > 880 :
                for enum2, vilain2 in enumerate(self.vilains):
                    vilain2.move_down(self.canvas)
                    vilain2.move_left(self.canvas)
                self.vil_dir = 0
            if coords[0] > 30 and coords[0] < 880 :
                if dir == 0 :
                    vilain.move_left(self.canvas)
                if dir == 1 :
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
    
    def Lot_of_shots(self, event):
        print(self.canvas.coords(self.vilains)[:2])
    
    # triple shoot striaght up
    def go_v(self, event):
        # only want the first two coords
        x, y = self.canvas.coords(self.ship)[:2]        
        #up
        self.bullets.append(Bullet(self.canvas, x, y, "green", (0, -5)))
        self.bullets.append(Bullet(self.canvas, x - 50, y, "green", (0, -5)))
        self.bullets.append(Bullet(self.canvas, x + 50, y, "green", (0, -5)))


def main():
    root = tk.Tk()
    app = App(root)
    root.title('SpaceInvader')
    txt1 = tk.Label(root,text = 'Score :')
    txt2 = tk.Label(root,text = 'Record :')
    txt3 = tk.Label(root,text = 'Vies: 3')
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