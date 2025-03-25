# Cat assets by ToffeeCraft on itch.io

import random
import tkinter as tk
import os
import sys

def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# Actual pet setup
class Pet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.spd = 25

        # Root setup
        self.root = tk.Tk()
        self.root.geometry('128x128')
        self.root.overrideredirect(True)
        self.root.wm_attributes('-topmost', True)
        
        # Make background transparent
        try:
            self.root.wm_attributes('transparentcolor', 'green')
        except:
            pass

        # Get screen limitations
        self.screen_w = self.root.winfo_screenwidth()
        self.screen_h = self.root.winfo_screenheight()

        # Animations setup
        self.idle_r = [tk.PhotoImage(file=get_resource_path('art/still0_r.png')).zoom(4, 4),
                       tk.PhotoImage(file=get_resource_path('art/still1_r.png')).zoom(4, 4)] * 2
        
        self.idle_l = [tk.PhotoImage(file=get_resource_path('art/still0_l.png')).zoom(4, 4),
                       tk.PhotoImage(file=get_resource_path('art/still1_l.png')).zoom(4, 4)] * 2

        self.walk_r = [tk.PhotoImage(file=get_resource_path('art/walk0_r.png')).zoom(4, 4),
                       tk.PhotoImage(file=get_resource_path('art/walk1_r.png')).zoom(4, 4)]

        self.walk_l = [tk.PhotoImage(file=get_resource_path('art/walk0_l.png')).zoom(4, 4),
                       tk.PhotoImage(file=get_resource_path('art/walk1_l.png')).zoom(4, 4)]
        
        self.jumpprep_r = [tk.PhotoImage(file=get_resource_path('art/jump0_r.png')).zoom(4, 4),
                           tk.PhotoImage(file=get_resource_path('art/jump1_r.png')).zoom(4, 4)]
        
        self.jumpprep_l = [tk.PhotoImage(file=get_resource_path('art/jump0_l.png')).zoom(4, 4),
                           tk.PhotoImage(file=get_resource_path('art/jump1_l.png')).zoom(4, 4)]

        self.jump_r = [tk.PhotoImage(file=get_resource_path('art/leap0_r.png')).zoom(4, 4)] * 2
        self.jump_l = [tk.PhotoImage(file=get_resource_path('art/leap0_l.png')).zoom(4, 4)] * 2

        self.pet_r = [tk.PhotoImage(file=get_resource_path(f'art/pet{i}_r.png')).zoom(4, 4) for i in range(5)]
        self.pet_l = [tk.PhotoImage(file=get_resource_path(f'art/pet{i}_l.png')).zoom(4, 4) for i in range(5)]

        # Dictionary of all animations
        self.anims = {0: self.idle_r, 1: self.walk_r, 2: self.jumpprep_r,
                      3: self.idle_l, 4: self.walk_l, 5: self.jumpprep_l,
                      6: self.jump_r, 7: self.jump_l, 8: self.pet_r, 9: self.pet_l}

        # Cat setup
        self.cat = tk.Label(self.root, image=self.idle_r[0], bg='green')
        self.cat.pack()
        
        # Let cat be clicked
        self.clicked = False
        self.cat.bind('<Button-1>', lambda e: self.on_click())
        self.cat.bind('<ButtonRelease-1>', lambda e: self.on_release())

    def on_click(self):
        self.clicked = True

    def on_release(self):
        self.clicked = False

    def next_anim(self, anim):
        if anim in [2, 5]: 
            return 6 if anim == 2 else 7
        return random.randint(0, 5)

    def next_frame(self, n, anim, r, rounds):
        if n < len(self.anims[anim]) - 1:
            n += 1
        elif r < rounds:
            n = 0
            r += 1
        else:
            n = 0
            anim = self.next_anim(anim)
        return n, anim, r, rounds

    def update(self, n, anim, x, y, r, rounds):
        n, anim, r, rounds = self.next_frame(n, anim, r, rounds)

        # Override animation if cat is clicked (except jumping)
        if self.clicked and anim not in [6, 7]:
            anim = 8 if anim in [0, 1, 2] else 9

        self.cat.configure(image=self.anims[anim][n])

        # Movement logic
        if anim == 1:
            self.x += self.spd
        elif anim == 4:
            self.x -= self.spd
        elif anim == 6:
            self.x += self.spd * 3
            self.y -= 50
        elif anim == 7:
            self.x -= self.spd * 3
            self.y -= 50

        # Apply gravity
        if self.y < self.screen_h - 128:
            self.y += 25

        # Prevent going offscreen
        self.x = max(0, min(self.x, self.screen_w - 128))

        # Move cat window
        try:
            self.root.geometry(f'+{int(self.x)}+{self.y}')
        except:
            pass

        # Schedule next update
        self.root.after(100, self.update, n, anim, x, y, r, rounds)

# Initialize and start the cat
cat = Pet(500, 600)
cat.update(0, 0, 10, 10, 0, 2)
cat.root.mainloop()