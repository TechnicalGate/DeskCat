#cat assets by ToffeeCraft on itch.io

import random
import tkinter as tk

#actual pet setup
class Pet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.spd = 25

        #root setup
        self.root = tk.Tk()
        self.root.geometry('128x128')
        self.root.overrideredirect(True) #hides top bar thing
        self.root.wm_attributes('-topmost', True) #keeps cat on top of screen
        #make background transparent
        try:
            #transparent color is windows only
            self.root.wm_attributes('transparentcolor', 'green')
        except:
            pass

        #get screen limitations
        self.screen_w = self.root.winfo_screenwidth()
        self.screen_h = self.root.winfo_screenheight()

        #animations setup
        self.idle_r = [tk.PhotoImage(file='art/still0_r.png').zoom(4,4),
                     tk.PhotoImage(file='art/still1_r.png').zoom(4,4),
                     tk.PhotoImage(file='art/still0_r.png').zoom(4,4),
                     tk.PhotoImage(file='art/still1_r.png').zoom(4,4)]
        
        self.idle_l = [tk.PhotoImage(file='art/still0_l.png').zoom(4,4),
                     tk.PhotoImage(file='art/still1_l.png').zoom(4,4),
                     tk.PhotoImage(file='art/still0_l.png').zoom(4,4),
                     tk.PhotoImage(file='art/still1_l.png').zoom(4,4)]
        
        self.walk_r = [tk.PhotoImage(file='art/walk0_r.png').zoom(4,4),
                     tk.PhotoImage(file='art/walk1_r.png').zoom(4,4)]

        self.walk_l = [tk.PhotoImage(file='art/walk0_l.png').zoom(4,4),
                     tk.PhotoImage(file='art/walk1_l.png').zoom(4,4)]
        
        self.jumpprep_r = [tk.PhotoImage(file='art/jump0_r.png').zoom(4,4),
                        tk.PhotoImage(file='art/jump1_r.png').zoom(4,4)]
        
        self.jumpprep_l = [tk.PhotoImage(file='art/jump0_l.png').zoom(4,4),
                        tk.PhotoImage(file='art/jump1_l.png').zoom(4,4)]

        self.jump_r = [tk.PhotoImage(file='art/leap0_r.png').zoom(4,4),
                       tk.PhotoImage(file='art/leap0_r.png').zoom(4,4)]

        self.jump_l = [tk.PhotoImage(file='art/leap0_l.png').zoom(4,4),
                       tk.PhotoImage(file='art/leap0_l.png').zoom(4,4)]

        self.pet_r = [tk.PhotoImage(file='art/pet0_r.png').zoom(4,4),
                      tk.PhotoImage(file='art/pet1_r.png').zoom(4,4),
                      tk.PhotoImage(file='art/pet2_r.png').zoom(4,4),
                      tk.PhotoImage(file='art/pet3_r.png').zoom(4,4),
                      tk.PhotoImage(file='art/pet4_r.png').zoom(4,4)]

        self.pet_l = [tk.PhotoImage(file='art/pet0_l.png').zoom(4,4),
                      tk.PhotoImage(file='art/pet1_l.png').zoom(4,4),
                      tk.PhotoImage(file='art/pet2_l.png').zoom(4,4),
                      tk.PhotoImage(file='art/pet3_l.png').zoom(4,4),
                      tk.PhotoImage(file='art/pet4_l.png').zoom(4,4)]

        #dictionary of all animations to make my life easier
        self.anims = {0:self.idle_r,
                      1:self.walk_r,
                      2:self.jumpprep_r,
                      3:self.idle_l,
                      4:self.walk_l,
                      5:self.jumpprep_l,
                      6:self.jump_r,
                      7:self.jump_l,
                      8:self.pet_r,
                      9:self.pet_l}

        #cat setup
        self.cat = tk.Label(self.root, image=self.idle_r[0], bg='green')
        self.cat.pack()
        #let cat be clicked
        self.clicked = False
        self.cat.bind('<Button-1>', lambda e:self.on_click())
        self.cat.bind('<ButtonRelease-1>', lambda e:self.on_release())

    def on_click(self):
        self.clicked = True
    def on_release(self):
        self.clicked = False

    def next_anim(self, anim):
        #special things (jumping)
        if anim == 2:
            return 6
        if anim == 5:
            return 7
        #random animation
        return random.randint(0, 5)

    def next_frame(self, n, anim, r, rounds):
        #if animation not finished, go to next frame
        if n < len(self.anims[anim]) - 1:
            n += 1
        #if animation finished but didnt loop enough, loop
        elif r < rounds:
            n = 0
            r += 1
        #if animation finished and looped enough, choose another animation
        else:
            n = 0
            anim = self.next_anim(anim)

        return n, anim, r, rounds

    def update(self, n, anim, x, y, r, rounds):
        #get frame and make cat actually appear to move
        n, anim, r, rounds = self.next_frame(n, anim, r, rounds)

        #pet cat overrides other animations except jump
        if self.clicked and anim not in [6,7]:
            #preserve cat facing direction
            if anim in [0,1,2]:
                anim = 8
            else:
                anim = 9
        #cat affection in on_click

        self.cat.configure(image=self.anims[anim][n])

        #movement
        if anim == 1:
            self.x += self.spd
        if anim == 4:
            self.x -= self.spd
        if anim == 6:
            self.x += self.spd*3
            self.y -= 50
        if anim == 7:
            self.x -= self.spd*3
            self.y -= 50
        
        #gravity
        if self.y < self.screen_h-128:
            self.y += 25
        
        #dont let cat go offscreen
        if self.x < 0:
            self.x = 0
        if self.x > self.screen_w-128:
            self.x = self.screen_w-128

        #actually move cat
        #try and except here so that even if the cat goes out of bounds the code wont crash
        try:
            self.root.geometry(f'+{str(int(self.x))}+{str(self.y)}')
        except:
            pass

        #update again
        self.root.after(100, self.update, n, anim, x, y, r, rounds)

cat = Pet(500,600)
cat.update(0, 0, 10, 10, 0, 2)

cat.root.mainloop()