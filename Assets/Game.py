import random

class Game:
    def __init__(self):
        self.words = self.__load_words()
        self.sorted_words = self.__load_sorted_words()
        self.target_word = self.words[random.randint(0, len(self.words) - 1)]
        self.guess_num = 0
        self.guess = ""

        print(self.target_word)

    # list of words to guess (about ~1k long, very common words)
    def __load_words(self):
        f = open("./Assets/targets.txt", "r")
        return f.read().split('\n')

    # list of words for the dictionary (sorted for binary search)
    def __load_sorted_words(self):
        f = open("./Assets/sorted.txt", "r")
        return f.read().split('\n')

    # Uses a binary search to find whether the word is valid
    def is_valid(self, guess):
        start = 0
        end = len(self.sorted_words) - 1

        while start <= end:
            middle = (start + end) // 2
            midpoint = self.sorted_words[middle]
            if midpoint > guess:
                end = middle - 1
            elif midpoint < guess:
                start = middle + 1
            else:
                return True
        return False

    # returns string array (e.g. ["green", "gray", "yellow", "gray", "gray"]) depending on the guess and target word
    def get_letter_colors(self):
        colors = [""]*5

        # tracks letter position in target word of cases we've already looked at
        target_word_handled = [False]*5

        # handle green/correct case
        for i in range(5):
            if self.guess[i] == self.target_word[i]:
                colors[i] = ("green")
                target_word_handled[i] = True

        for i in range(5):
            # if we already have a color for this index (greens only so far), skip
            if colors[i] != "":
                continue

            # handle gray/absent case
            if self.guess[i] not in self.target_word:
                colors[i] = ("gray")
            else:

                # handle yellow/present case 
                # have to do first unique occurance for double letter cases for words like 'tommy'
                current_letter_index = self.get_first_unique_occurance(self.guess[i], target_word_handled)
                if current_letter_index >-1:
                    colors[i] = ("yellow")
                    target_word_handled[current_letter_index] = True
                else:
                    # if there are no more occurances, we handled them all - the letter is gray
                    colors[i] = ("gray")
        
        return colors

    # finds first occurance of the given letter in the target word that HASN'T been handled yet 
    def get_first_unique_occurance(self, letter, target_word_handled):
        for i in range(5):
            if letter == self.target_word[i] and not target_word_handled[i]:
                return i

        return -1

    # getters and setters for reset 
    # can only reset/add character/delete last character from guess
    def get_guess(self):
        return self.guess

    def reset_guess(self):
        self.guess = ""

    def guess_add_character(self, char):
        self.guess += char

    def guess_backspace(self):
        self.guess = self.guess[:-1]

    # getter for the target word (word that we are trying to guess)
    def get_target_word(self):
        return self.target_word

    # getter for which guess we are on
    def get_guess_num(self):
        return self.guess_num

    # can only increase guess num after submitting a word
    def increment_guess_num(self):
        self.guess_num += 1