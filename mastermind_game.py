from tkinter import *
from random import *

class Menu(Toplevel):
    def __init__(self, parent):
        Toplevel.__init__(self, parent)
        self.title("MASTER MIND")
        self.geometry("330x490")
        self.configure(bg="black")
        self.label=Label(self, text="MASTER MIND", font=("Helvetica", 20, "bold"), fg="white", bg="black")
        self.label.place(relx=0.5, rely=1/3, anchor="center")
        
        self.btn_jouer=Button(self, text="JOUER", command=self.ouvrir_fenetre_Game)
        self.btn_jouer.place(relx=0.5, rely=2/3, anchor="center")
        
        self.btn_regles=Button(self, text="REGLES", command=self.ouvrir_fenetre_Rules)
        self.btn_regles.place(relx=0.5, rely=2/3 + 0.1, anchor="center")
        
    def ouvrir_fenetre_Game(self):
        self.withdraw()
        fenetre_Game=Game(self)
        fenetre_Game.protocol("WM_DELETE_WINDOW", self.retour_fenetre_Menu)
        
    def ouvrir_fenetre_Rules(self):
        self.withdraw()
        fenetre_Rules=Rules(self)
        fenetre_Rules.protocol("WM_DELETE_WINDOW", self.retour_fenetre_Menu)
        
    def retour_fenetre_Menu(self):
        self.deiconify()


class Game(Toplevel):    
    def __init__(self, parent):
        Toplevel.__init__(self, parent)
        self.title("MASTER MIND")
        self.config(bg="#000")
        self.geometry()
        
        self.canvas=Canvas(self, width=330, height=490, bg='ivory')
        self.canvas.pack(fill=BOTH, expand=True)
        
        self.status_label=Label(self, text="", bg="#000", fg="white")
        self.status_label.pack()

        self.result_label=None
        
        self.adversary_colours=[]
        self.button_colours=[]
        self.colours_given=[]
        self.round=0
        self.game_started=False
        self.game_over=False

        self.adversary_colours = self.generate_adversary_colours()
        
        for i, (text, color) in enumerate([('Violet', 'MediumPurple2'), ('Bleu', 'cornflower blue'), ('Vert', 'Seagreen1'), ('Jaune', 'yellow2'), ('Orange', 'salmon1'), ('Rose', 'HotPink1')]):
            colBtn=Button(self, text=text, bg=color, command=lambda i=i: self.func(i+1, self.canvas))
            colBtn.pack(side=LEFT, fill=BOTH, expand=True)
            self.button_colours.append(colBtn)

    def get_color_name(self, color_index):
        self.color_names={
            1:'MediumPurple2',
            2:'cornflower blue',
            3:'Seagreen1',
            4:'yellow2',
            5:'salmon1',
            6:'HotPink1'
        }
        return self.color_names.get(color_index)

    def reset_window(self):
        self.status_label.pack_forget()
        if self.result_label:
            self.result_label.pack_forget()
        if self.replay_button:
            self.replay_button.pack_forget()
        if self.menu_button:
            self.menu_button.pack_forget()
        for button in self.button_colours:
            button.pack_forget()

        self.status_label.pack()
        for button in self.button_colours:
            button.pack(side=LEFT, fill=BOTH, expand=True)

    def end_game(self, text):
        self.status_label.pack_forget()
        for button in self.button_colours:
            button.pack_forget()

        self.result_label=Label(self, text=text, bg="#000", fg="white", font=("Helvetica", 20, "bold"))
        self.result_label.pack(pady=20)

        self.replay_button=Button(self, text="REJOUER", command=self.replay)
        self.replay_button.pack()

        self.menu_button=Button(self, text="MENU", command=self.return_to_Menu)
        self.menu_button.pack()

    def create_square(self, canvas, row, col, color, row_offset=0, col_offset=0, user_colors=False):
        if user_colors:
            col_offset+=1
        x1=col*40+10+col_offset*40
        y1=(12-row)*40+10-row_offset*40
        x2=x1+30
        y2=y1+30
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)

    def update_status_label(self, text):
        self.status_label.config(text=text)

    def generate_adversary_colours(self):
        adversary_colours=[]
        for aleatory in range(4):
            adversary_colours.append(randint(1, 6))
        print(adversary_colours)
        return adversary_colours
    
    def func(self, button_press, canvas):   # ACE : nom de fonction trop générique
        self.game_started=True
        
        if self.round>=10:
            self.game_over=True
            self.end_game("Dommage...")
            return

        if len(self.colours_given[:])>=4:
            self.round+=1
            self.colours_given.clear()
            self.update_status_label("")
            
        else:
            if self.game_started!=False:
                self.colours_given.append(button_press)
                self.create_square(canvas, self.round + 1, len(self.colours_given), self.get_color_name(button_press), user_colors=True)

                if len(self.colours_given)==4 and len(self.adversary_colours)==4:
                    for j in [0, 1, 2, 3]:
                        if j==0 or j==1:
                            if self.colours_given[j]==self.adversary_colours[j]:
                                self.create_square(canvas, self.round, j + 1, 'black', row_offset=1, col_offset=-1)
                            elif self.colours_given[j] in self.adversary_colours:
                                self.create_square(canvas, self.round, j + 1, 'red', row_offset=1, col_offset=-1)
                        if j==2 or j==3:
                            if self.colours_given[j]==self.adversary_colours[j]:
                                self.create_square(canvas, self.round, j + 5, 'black', row_offset=1, col_offset=-1)
                            elif self.colours_given[j] in self.adversary_colours:
                                self.create_square(canvas, self.round, j + 5, 'red', row_offset=1, col_offset=-1)
                            
                    if all(element1==element2 for element1, element2 in zip(self.colours_given, self.adversary_colours)):
                        self.game_over=True
                        self.end_game("BRAVO !")
                        for button in self.button_colours:
                            button.config(state='disabled')
                        return
                    else:
                        self.update_status_label("Réessaye !")
                        self.game_started=True
                        self.after(500, self.next_turn)
                    

    def replay(self):
        self.round=0
        self.game_started=False
        self.game_over=False

        self.result_label.pack_forget()
        self.replay_button.pack_forget()
        self.menu_button.pack_forget()

        self.status_label.pack()
        for button in self.button_colours:
            button.pack()
            button.config(state='normal')

        self.reset_window()
        
        self.canvas.delete("all")
        
        self.colours_given.clear()

        self.adversary_colours = self.generate_adversary_colours()
        
    def return_to_Menu(self):
        self.adversary_colours.clear()
        self.adversary_colours=self.generate_adversary_colours()
        print(self.adversary_colours)
        self.colours_given.clear()
        self.withdraw()
        fenetre_Menu=Menu(self)
        fenetre_Menu.protocol("WM_DELETE_WINDOW", fenetre_Menu.retour_fenetre_Menu)

    def next_turn(self):
        if self.game_over:
            return
        self.update_status_label("")
        button_press=0
        self.func(button_press, canvas=None)


class Rules(Toplevel):
    def __init__(self, parent):
        Toplevel.__init__(self, parent)
        self.title("MASTER MIND")
        self.config(bg="#000")
        self.geometry("330x490")
        
        self.configure(bg="black")
        self.label=Label(self, text="REGLES", font=("Helvetica", 20, "bold"), fg="white", bg="black")
        self.label.place(relx=0.5, rely=0.05, anchor="center")
        
        self.texte=Label(self, text="L'ordinateur a choisi une combinaison de 4 couleurs. Ton but ? Le trouver. Pour cela tu as le choix entre 6 couleurs et tu as 10 tours maximum.\n\nLorsque tu as mis la bonne couleur à la bonne place, un carré noir s'affiche. Si tu as mis une bonne couleur mais à la mauvaise place, un carré rouge s'affiche. Sinon, rien ne s'affiche.\n\nL'affichage se fait dans cet ordre là :\nCorrespondance 1, 2 ; couleurs choisies 1, 2, 3, 4 ; correspondance 3, 4.\n\nBonne chance !",
                    font=("Helvetica", 12), fg="white", bg="black", wraplength=310)
        self.texte.place(relx=0.5, rely=0.5, anchor="center")
        
        self.btn_menu=Button(self, text="MENU", command=self.retour_fenetre_Menu)
        self.btn_menu.place(relx=0.3, rely=0.9, anchor="center")
        
        self.btn_jouer=Button(self, text="JOUER", command=self.ouvrir_fenetre_Game)
        self.btn_jouer.place(relx=0.7, rely=0.9, anchor="center")
        
    def retour_fenetre_Menu(self):
        self.withdraw()
        fenetre_Menu=Menu(self)
        fenetre_Menu.protocol("WM_DELETE_WINDOW", self.retour_fenetre_Rules)
        
    def ouvrir_fenetre_Game(self):
        self.withdraw()
        fenetre_Game=Game(self)
        fenetre_Game.protocol("WM_DELETE_WINDOW", self.retour_fenetre_Rules)
        
    def retour_fenetre_Rules(self):
        self.deiconify()


root=Tk()
fenetre_Menu=Menu(root)
root.withdraw()
root.mainloop()
