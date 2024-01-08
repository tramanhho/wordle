import tkinter as tk
from tkinter.font import BOLD, Font
import json

class Keyboard:
    def __init__(self, master, screen_width, screen_height):
        self.master = tk.Toplevel(master)
        self.master.title("Keyboard")

        keyboard_width = 820 
        keyboard_height = 220 

        # calculate x and y coordinates for the keyboard game
        x = (3 * screen_width/4)  - (keyboard_width/2)
        y = (screen_height/4) - (keyboard_height/2)

        # set height/width + x/y coords 
        self.master.geometry('%dx%d+%d+%d' % (keyboard_width, keyboard_height, x, y))


        self.keys = [] 
        #example input: 
        # {
        #      letter: "A",
        #      button: { Tkinter Button Object },
        #      status: one of "unguessed", "absent", "present", "correct"
        # }

        # keyboard array that is used to during initialization to populate the self.keys[] object.
        # when initialization finishes, it is empty and garbage collected
        self.keyboard = [
            'Q', 'W','E', 'R','T', 'Y', 'U', 'I',  'O', 'P',
              'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L',
                 'Z', 'X', 'C', 'V', 'B', 'N', 'M']

        # initialize the first row of buttons (qwertyuiop)
        for i in range(10):
            self.make_key(1, (i*2))
           
        # initialize the second row of buttons (asdfghjkl)
        for i in range(9):
            self.make_key(2, (1+(i*2)))

        # initialize the third row of buttons (zxcvbnm)
        for i in range(7):
            self.make_key(3, (3+(i*2)))
           
        # initialize the backspace and enter buttons
        for i in range(2):
            if i == 0: 
                col=0
                text="➤"
            else: 
                col=17
                text="⌫"
            btn = tk.Button(self.master, text=text, font=("Open Sans Bold", 20),width = 6, height =1)
    
            btn.grid(row=3, column=col, columnspan=3, padx=1, pady=2)

    # Keyboard Button Factory. uses the keyboard array and pops each letter from it as it processes
    def make_key(self, r, c):
        letter = self.keyboard[0]
        btn = tk.Button(self.master, text=letter, font=("Open Sans Bold", 20),width = 4, height =1)
        self.keys.append( {"letter": letter, "button": btn, "status": "unguessed"} )
        self.keyboard.pop(0)
        btn.grid(row=r, column=c, columnspan=2, padx=2, pady=2)

    # When players guess, it changes the key color with their running guess progress
    def change_key_color(self, key, color):
        match color:
            case "green": 
                new_color  = "#218751"
                new_status = "correct"

            case "yellow": 
                new_color  = "#D18B31"
                new_status = "present"

            case "gray": 
                new_color  = "#141414"
                new_status = "absent"

        # find the corresponding key/letter in the keys[] object/dictionary array
        curr_key = next(item for item in self.keys if item["letter"] == key.upper())

        # ONLY overwrite if the color isn't green (i.e. correct guess in the correct location)
        if curr_key["status"] != "correct":
            curr_key["button"].config(bg=new_color)
            curr_key["status"] = new_status

            # absent keys should be "grayed out" for a more intuitive experience
            if curr_key["status"] == "absent":
                absent_text_color = "#565658"
                curr_key["button"].config(fg=absent_text_color)
