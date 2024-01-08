import tkinter as tk
from tkinter.font import BOLD, Font
from Assets.Game import Game
from Assets.Keyboard import Keyboard

class Wordle:
    # The following constants are all colors that the letter boxes can be during gameplay. 
    # tuples bc i like fade animations. saving the specific hex codes bc a function to calculate 
    # them based on opacity/HSL values is Too Much Work 
    LETTER_GREENS=("#1E4932", "#1F583A", "#206C44", "#218751")
    LETTER_YELLOWS=("#684B25", "#825A28", "#A46F2C", "#D18B31")
    LETTER_GRAYS=("#212121", "#232323", "#262626", "#292929")
    LETTER_ENABLEDS=("#151515", "#171717", "#1A1A1A", "#1C1C1C")
    LETTER_FOCUSED=("#1A1A1A", "#222222", "#2B2B2D", "#363638")

    # this is a fade in fade out so it essentially goes from white to red back to white again
    LETTER_REDS=( 
        "#FFC7D1", "#FC8DA2", "#F25270", 
        "#E81C41", "#E81C41", "#E81C41",
        "#F25270", "#FC8DA2", "#FFC7D1", 
        "#FFFFFF")

    # handles the border fading to the next respective letter color
    BORDER_GREENS=("#4c5f57", "#406a55", "#317853", "#218751")
    BORDER_YELLOWS=("#6c6051", "#896c48", "#ab7b3d", "#D18B31")
    BORDER_GRAYS=("#4e4e50", "#434345", "#373738", "#292929")
    BORDER_DEFAULTS=("#282828", "#3b3b3c", "#4a4a4c", "#565658")

    # defaults for letter colors (i.e. not guessed yet)
    BG_COLOR="#1C1C1C"
    BG_COLOR_FOCUSED="#363638"
    COLOR_DISABLED="#141414"
    BORDER_COLOR_DEFAULT="#565658"

    # default font family and size
    TEXT_DEFAULT = {
        'family': "Open Sans Bold",
        'size': 20
    }

    # central object! this holds ALL the letter box Labels and is updated in some way (bounce, color change, etc),
    # every time a key is pressed
    letter_labels = [[""] * 5 for i in range(6)]

    # initialize! creates both the wordle gameplay and keyboard guess tracking windows
    def __init__(self, master, screen_width, screen_height):
        self.game = Game()
        self.keyboard = Keyboard(master, screen_width, screen_height)
        self.master = master

        frame = tk.Frame(master, width = 550, height = 800, pady=100)
        frame.pack(side=tk.TOP)
        frame.pack_propagate(0)

        # Initialize letter boxes
        for i in range(6):
            for j in range(5): 
                bgColor = ""
                fgColor = ""
                # rows 2-6 are disabled and the first square is focused
                # for more intuitive user experience
                if i == 0: 
                    if j==0:
                        bgColor = self.BG_COLOR_FOCUSED
                    else:
                        bgColor = self.BG_COLOR
                    fgColor = self.BORDER_COLOR_DEFAULT
                else: 
                    bgColor = self.COLOR_DISABLED
                    fgColor = self.COLOR_DISABLED

                # the label that will hold each letter. set it to defaults with bg/border color based on 
                # index as described above
                letterBox = tk.Label(frame, 
                                     compound='c',
                                     text="", font=Font(family=self.TEXT_DEFAULT["family"], 
                                                        size=self.TEXT_DEFAULT["size"]), 
                                     width=4, height=2, 
                                     bg=bgColor,
                                     highlightbackground=fgColor, highlightthickness=2)

                # place the letter label on the screen
                letterBox.place(x=50+(j*90), y=(i*110)-30)

                # add the letter to the central array for future modification
                self.letter_labels[i][j] = letterBox
        
        # makes it so that pressing key on the actual keyboard (not the virtual/onscreen one) 
        # will perform expected behavior (i.e. add a letter, subtract a letter, or submit guess)
        for i in range(97, 123):
            master.bind(chr(i), self.add_letter)
        
        self.master.bind("<BackSpace>", self.backspace)
        self.master.bind("<Return>", self.submit_guess)
    
    # called when a letter on the physical keyboard is pressed. 
    # adds a letter with a bounce + focuses the next letter box
    def add_letter(self, e):
        guess_num = self.game.get_guess_num()
        curr_letter = len(self.game.get_guess())

        # only perform behavior if we are on the fourth letter or less 
        # i.e. don't add letters when your guess is already 5 letters long
        if curr_letter <= 4:

            # bounce + add letter
            self.letter_type_bounce(guess_num, curr_letter)
            self.letter_labels[guess_num][curr_letter].config(bg=self.BG_COLOR, text=e.char.upper())
            self.game.guess_add_character(e.char)

            # see if we need to focus the next box on the line
            curr_letter += 1
            if curr_letter <= 4:
                self.letter_labels[guess_num][curr_letter].config(bg=self.BG_COLOR_FOCUSED)

    # called when the backspace key is pressed
    # deletes the letter + moves focus 
    def backspace(self, e):
        curr_letter = len(self.game.get_guess())
        last_letter = curr_letter - 1
        guess_num = self.game.get_guess_num()

        # only perform behavior if we are on the first letter or more
        # i.e. only delete a letter if there IS a letter TO delete
        if curr_letter > 0:
            self.game.guess_backspace()
            self.letter_labels[guess_num][last_letter].config(bg=self.BG_COLOR_FOCUSED, text="")

            # will only be able to access curr_letter if letter is less than 5
            if curr_letter < 5:
                self.letter_labels[guess_num][curr_letter].config(bg=self.BG_COLOR, text="")
            else:
                self.letter_labels[guess_num][last_letter].config(text="")
    
    # called when the enter key is pressed
    # submits the guess and either 
    # 1) moves on with the game + finishes if needed or 
    # 2) tells you your guess is invalid
    def submit_guess(self, e):
        # get relevant info from Game class
        guess = self.game.get_guess()
        guess_num = self.game.get_guess_num()
        target_word = self.game.get_target_word()

        # only check words that are 5 letters
        if len(guess) != 5: return

        # 1) if you guessed the word, finish the game and win
        # 2) if you didn't guess the word, either move onto the next guess or say YOU LOST 
        # 3) if your guess isn't even valid, flash red
        if guess == target_word: self.finish_game(guess_num)
        elif self.game.is_valid(guess): self.next_word(guess_num)
        else: self.show_not_in_dictionary(guess_num) 

    # bounce on letter entry
    def letter_type_bounce(self, i, j):
        self.bounce_grow(i, j)

    """ NOTE!!!!!!!!!!!!!!!!!!!!!! 
    some helper functions (bounce_grow, bounce_shrink, show_not_in_dictionary, 
    change_letter_color_fade) utilize after(n, function), which is called on a root and 
    puts a given function on a queue, calling it after n miliseconds. this is why anything 
    "animated" (i.e. changing color, bouncing, etc) is recursive -- after can ONLY call a 
    function and can't be used in a loop like you would use a sleep() function """

    # increase font size recursively (letter box grows/shrinks with font size)
    def bounce_grow(self, i, j, count = 0):
        if count < 3:

            # the size depending on the count/time simulates an ease in  
            size = (20 + count)
            self.letter_labels[i][j].config(font=(self.TEXT_DEFAULT["family"], size))
            count += 1;
            self.master.after(10, lambda: self.bounce_grow(i, j, count))
        else:
            self.bounce_shrink(i, j)

    # decrease font size recursively (letter box grows/shrinks with font size)
    def bounce_shrink(self, i, j, count = 0):
        if count < 3:

            # the size depending on the count/time simulates an ease out
            size = (22 - count)
            self.letter_labels[i][j].config(font=(self.TEXT_DEFAULT["family"], size))
            count += 1;
            self.master.after(10, lambda: self.bounce_shrink(i, j, count)) 

    # flash/glow the whole guess red to show INVALID !!!!!!!!!!!!!
    def show_not_in_dictionary(self, row, count = 0):
        if count < 10:
            for i in range(5):
                self.letter_labels[row][i].config(fg=self.LETTER_REDS[count])
            count += 1;
            self.master.after(37, lambda: self.show_not_in_dictionary(row, count))

    # move onto the next word or end the game, telling the player they LOST
    def next_word(self, guess_num):

        # get colors of the guess (i.e. gray/green/yellow depending on guess validity)
        colors = self.game.get_letter_colors()

        # first, change colors on the helper keyboard
        for i in range(5):
            self.keyboard.change_key_color(self.game.get_guess()[i], colors[i])

        # now, we track both 
        # last_row (the row of the word we JUST guessed, changing to respective letter color) 
        # current_row (the next row, to switch from disabled to enabled/focused)
        last_row = guess_num
        current_row = guess_num + 1
        self.game.increment_guess_num()
        self.game.reset_guess()

        # change row of guess to respective colors
        self.change_letter_color_fade(last_row, colors)

        # if user hasn't lost yet, enable next row
        if (guess_num < 5):
            self.letter_labels[current_row][0].config(bg=self.BG_COLOR_FOCUSED)
            self.change_letter_color_fade(current_row)
        else:
            self.finish_game(6) 

    """
        @change_letter_color_fade: recursively animates letter box fades
        @self = frame to draw board on 
        @row = row to change color of
        @colors = base colors to change to, optional if enabling next row
        @t = time/how far along we are in the "timeline" (starts at 0, ends at 4)
    """
    def change_letter_color_fade(self, row, colors = None, t = 0):
        # if we're at time 4, stop
        if t >= 4:
            return

        for i in range(5):
            # set colors for if we're changing next row to enabled/focused
            if colors == None:
                bg_color     = self.LETTER_FOCUSED[t] if i == 0 else self.LETTER_ENABLEDS[t]
                border_color = self.BORDER_DEFAULTS[t]

            # set colors for if we're changing current row to new letter colors
            else:
                colorIndex = colors[i]

                match colorIndex:
                    case "gray": 
                        bg_color     = self.LETTER_GRAYS[t]
                        border_color = self.BORDER_GRAYS[t]
                    case "yellow": 
                        bg_color     = self.LETTER_YELLOWS[t]
                        border_color = self.BORDER_YELLOWS[t]
                    case "green": 
                        bg_color     = self.LETTER_GREENS[t]
                        border_color = self.BORDER_GREENS[t]
            
            # actually change the colors of the labels
            self.letter_labels[row][i].config(bg=bg_color, highlightbackground=border_color)

        # move on with the next step of the animation
        t += 1;
        self.master.after(30, lambda: self.change_letter_color_fade(row, colors, t)) 

    # SO YOU'VE WON/LOST.
    def finish_game(self, guess_num):

        # since we skipped straight to finish_game for winning, we have to handle colors here
        if (guess_num < 6):
            self.change_letter_color_fade(guess_num, ["green"]*5)
            for i in range(5):
                self.keyboard.change_key_color(self.game.get_target_word()[i], 'green')

        # text changes based on how many guesses you took to get the word
        match (guess_num):
            case 0: text = "Genius!"
            case 1: text = "Magnificent"
            case 2: text = "Impressive"
            case 3: text = "Splendid"
            case 4: text = "Great"
            case 5: text = "Phew..."
            case 6: text = self.game.get_target_word()
        
        # calculate the width of the box for the text above
        canvasWidth = (len(text) * 18) + 50

        # put the text on screen with white bg
        top = tk.Canvas(self.master, bg="white", height=75, width=canvasWidth, bd=0, highlightthickness=0)
        top.create_text((canvasWidth // 2), 37, text=text.upper(), fill=self.COLOR_DISABLED, font=(self.TEXT_DEFAULT["family"], 25))
        top.place(x=275 - (canvasWidth // 2), y=150)

        # DESTROY!!! after 5 seconds
        self.master.after(5000, self.master.destroy)