import random
import colorama
from colorama import Fore
colorama.init()
HANGMAN_ASCII_ART=""" Welcome to the game Hangman\n
  _    _                                         
 | |  | |                                        
 | |__| | __ _ _ __   __ _ _ __ ___   __ _ _ __  
 |  __  |/ _` | '_ \ / _` | '_ ` _ \ / _` | '_ \ 
 | |  | | (_| | | | | (_| | | | | | | (_| | | | |
 |_|  |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|
                      __/ |                      
                     |___/
"""
#MAX_TRIES=random.randint(5,10) #use for a random numbers of tries
MAX_TRIES=6
NUM_OF_TRIES=0

HANGMAN_PHOTOS= {
    0:"x-------x",
    1:""" 
    x-------x
    |
    |
    |
    |
    |""",
    2:"""
    x-------x
    |       |
    |       0
    |
    |
    |""",
    3:"""
    x-------x
    |       |
    |       0
    |       |
    |
    |""",
    4:"""
    x-------x
    |       |
    |       0
    |      /|\\
    |
    |""",
    5:"""
    x-------x
    |       |
    |       0
    |      /|\\
    |      /
    |""",
    6:"""
    x-------x
    |       |
    |       0
    |      /|\\
    |      / \\
    |"""
}
def open_game():
    print(Fore.RED + HANGMAN_ASCII_ART , "number of tries you have: ", MAX_TRIES, '\033[39m')
    return None

def choose_word(file_path,index):
    """
    Choose word from a text file. the chosen word appears in the file by the index parameter.
    :param file_path: path location of the file on the computer.
    :param index: selected word's index.
    :type index: int.
    :return: the chosen word from the file.
    :rtype: string.
    """
    # found_words = {}  # empty dictionary
    with open(file_path, 'r') as f:
        lines = (f.read()).split()
        print("file content: ", lines)
        print(index)
        while index > len(lines):
            index = index - len(lines)
    ChosenWord = lines[index-1]
    return ChosenWord

def print_hangman(num_of_tries):
    print(HANGMAN_PHOTOS[num_of_tries], "\n")

def show_blocked_word(chosen_word):
    """
    The function prints amount of under lines by the amount of the letters of the chosen word.
    :param chosen_word: the chosen word from a text file.
    :type chosen_word: string.
    :return: NONE.
    """
    len_of_word = len(chosen_word)
    print("_ " * len_of_word)

def start_game(chosen_word):
    """
        The function get a letter from the user and print the hangman depending on the user position in the current round.
        if the user ended the game the function will print his state depending on the user success or lose.
        :param chosen_word: the chosen word from a text file.
        :type chosen_word: string.
        :return: NONE.
        """
    list_of_guessed_letters=[]
    global NUM_OF_TRIES
    while(NUM_OF_TRIES< MAX_TRIES):
        letter_guessed=input("Please guess a letter: ")
        if(try_update_letter_guessed(letter_guessed.lower() , list_of_guessed_letters)==True):
            if(not(letter_guessed.lower() in chosen_word.lower())):
                NUM_OF_TRIES = NUM_OF_TRIES + 1
                print("TRY AGAIN :(")
                print_hangman(NUM_OF_TRIES)
                if(NUM_OF_TRIES==MAX_TRIES):
                    print(Fore.RED + "YOU LOSE",'\033[39m',"\nyour guess was: ",
                          show_hidden_word(chosen_word, list_of_guessed_letters),"\nthe chosen word is: ", chosen_word)
                    return
            print(show_hidden_word(chosen_word, list_of_guessed_letters))
            if(check_win(chosen_word, list_of_guessed_letters)==True):
                print(Fore.BLUE + "YOU WIN")
                return


def is_valid_input(letter_guessed):
    """
    The function check the valid of a letter by it's length and by it's size
    and check if the letter is an alphabet letter.
    The function return FALSE if the letter is not an alphabet or lenght of 1.
     The function return TRUE if the letter is an alphabet letter and lenght of 1.
    :param letter_guessed: a letter from the user.
    :type letter_guessed: char.
    :return: True or False.
    :rtype: BOOL.
    """
    if( (len(letter_guessed)>1) or (not(letter_guessed.islower())) and (not(letter_guessed.isupper())) ):
        return False
    else:
        return True

def check_valid_input(letter_guessed, old_letters_guessed):
    """
    The function check if the letter is valid and if the letter appears on the guessed list.
    :param letter_guessed: the letter from the user.
    :param old_letters_guessed: list of guessed letters from the user.
    :return: True or False.
    :rtype: BOOL.
    """
    flag_of_valid_input = is_valid_input(letter_guessed)
    if (((flag_of_valid_input == True) and ((letter_guessed in old_letters_guessed) == False))):
        return True
    else:
        print(Fore.YELLOW + "WRONG LETTER", '\033[39m')
        return False

def try_update_letter_guessed(letter_guessed, old_letters_guessed):
    """
        The function add the guessed letter from the user to the list of the guesses letters and print the updated list.
        :param letter_guessed: the letter from the user.
        :param old_letters_guessed: list of guessed letters from the user.
        :return: True or False.
        :rtype: BOOL.
    """
    temp=check_valid_input(letter_guessed, old_letters_guessed)
    if( temp==True ):
        if(letter_guessed not in old_letters_guessed):
            old_letters_guessed.append(letter_guessed)
            return True
        else:
            temp=False
    else:
        if(len(old_letters_guessed)!=0):
            print(*sorted(old_letters_guessed), sep=' -> ')
        return False


def show_hidden_word(secret_word, old_letters_guessed):
    """
        The function print the chosen word by each correct letter from the user and print blink space of the other left letters of the word.
        :param secret_word: the word that has been chosen from the file.
        :param old_letters_guessed: list of guessed letters from the user.
        :return: string
        """
    new_list=list()
    for letter in secret_word:
        if letter in old_letters_guessed:
            new_list.append(letter + " ")
        else:
            new_list.append("_ ")
        result = ''.join(new_list)
    return result

def check_win(secret_word, old_letters_guessed):
    for letter in secret_word:
            if(letter not in old_letters_guessed):
             return False
    return True

def main():
    open_game()
    # C:\Users\maorh\Desktop\לימודים\פייתון\for game.txt
    chosen_word=choose_word(input("Please enter path of a text file: "), int(input("Please enter an integer number: ")))
    #print("the chosen word is: ", chosen_word)
    print("Let’s start!\n")
    print_hangman(NUM_OF_TRIES)
    show_blocked_word(chosen_word)
    start_game(chosen_word)

if __name__ == "__main__":
    main()