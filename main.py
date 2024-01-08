from tkinter import Tk
from wordle import Wordle

wordle = Tk()
wordle.title("Wordle")

wordle_width = 550 
wordle_height = 800 

# get screen width and height to help calculate where to put the wordle window
screen_width = wordle.winfo_screenwidth() 
screen_height = wordle.winfo_screenheight() 

# calculate x and y coordinates for the wordle game
x = (screen_width/4)  - (wordle_width/2)
y = (screen_height/2) - (wordle_height/2)

# set height/width + x/y coords 
wordle.geometry('%dx%d+%d+%d' % (wordle_width, wordle_height, x, y))

# set game colors
wordle.call("source", "Assets/SunValley/sun-valley.tcl")
wordle.call("set_theme", "dark")

# open window + start game (passing in the screen width/height to help calculate where to put the keyboard window)
window = Wordle(wordle, screen_width, screen_height)

# required to make tkinter programs work
wordle.mainloop()