import random
import sys
import requests


def try_to_guess(word):
    """Guess letters from word until
    you are out of tries"""

    # set number of tries based on word length
    if 4 < len(word) < 7:
        tries = 4
    elif 7 < len(word) < 12:
        tries = 8
    else:
        tries = 12
    
    # create placeholder word eg: ---
    placeholder = ['-' for _ in range(len(word))]
    
    # list to check if letter was already guessed
    guesses = []

    while tries > 0:
        print('\n' + ''.join(placeholder))
        letter = str(input(f"Input a letter: "))

        # only one lower case alphanum character
        if len(letter) > 1:
            print("You should input a single letter")
        elif not letter.isalnum() or not letter.islower():
            print("It is not an ASCII lowercase letter")
    
        elif letter in guesses:
            print("You already typed this letter")     
        elif letter not in word:
            print("No such letter in the word")
            tries -= 1
            
        # we have a good letter
        else:
            for i, v in enumerate(word):
                
                if v == letter:
                    placeholder[i] = letter
                    
                if ''.join(placeholder) == word:
                    print()
                    print(''.join(placeholder))
                    print("You guessed the word!\nYou survived!")
                    return
                
        guesses.append(letter)
        
    else:
        print("You lost!")
        print(f"The word was {word}")


def start_game():
    """Start game"""
    print("----H A N G M A N----")
    
    # select a list of words from svnweb, check if it is still working
    print("Creating list of words")
    word_site = "https://svnweb.freebsd.org/base/head/share/dict/web2?view=co"
    response = requests.get(word_site)
    word_list = response.content.decode("utf-8") .splitlines()
    # select only words with 4 ore more letters
    word_list = [e.lower() for e in word_list if 4 < len(e)] 
    
    
    while True:
        option = str(input('Type "play" to play the game, "exit" to quit: '))
        if option == "play":
            word = random.choice(word_list)
            try_to_guess(word)
        elif option == "exit":
            sys.exit()


if __name__ == '__main__':
    start_game()
