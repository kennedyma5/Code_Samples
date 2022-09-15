
import random
from random import shuffle
import string
from google_images_search import GoogleImagesSearch
from PIL import Image
import glob
import os
import numpy as np

gis = GoogleImagesSearch('AIzaSyAxRrLIvUkSq41rvzXMYUwbJeEZxFjgnXQ', '974b4885b8dc64b81')
WORDLIST_FILENAME = "animals.txt"

def image_search(word):
    if not os.path.exists('images'):
        os.makedirs('images')

    files = glob.glob('images/*')
    for f in files:
        os.remove(f)

    _search_params = {
        'q': word,
        'num': 3,
        'fileType': 'jpg',
        'safe': 'safeUndefined',
        'imgType': 'imgTypeUndefined',
        'imgSize': 'imgSizeUndefined',
        'imgDominantColor': 'imgDominantColorUndefined',
        'imgColorType': 'imgColorTypeUndefined'
    }

    gis.search(search_params=_search_params, path_to_dir='images/', custom_image_name='image')

    return

def choose_image(word):
    image_search(word)

    image_list = []
    for filename in glob.glob('images/*'):
        image_list.append(filename)

    return random.choice(image_list)

def image_section_array(word):
    length = len(word)
    image_sections = list(range(1, length + 1))
    shuffle(image_sections)

    return image_sections

def show_image(path, image_section_array, word, correct_guesses):
    img = Image.open(path).convert('RGB')
    img_arr = np.array(img)
    divider = int((img.width)/len(word))

    for i in range(len(word)-correct_guesses):
        img_arr[0:, (image_section_array[i]-1)*divider: image_section_array[i]*divider] = (255, 255, 255)
        img = Image.fromarray(img_arr)
    img.show()

    return

def load_words():
    print("Loading word list from file...")
    file = WORDLIST_FILENAME
    with open(file) as f:
        wordlist = [line.rstrip('\n').lower() for line in f]
    print("  ", len(wordlist), "words loaded.")
    return wordlist

wordlist = load_words()


def choose_word(wordlist):
    return random.choice(wordlist)


def is_word_guessed(secret_word, letters_guessed):
    for letter in secret_word:
      if letter not in letters_guessed:
        return False
    return True


def get_guessed_word(secret_word, letters_guessed):
    users_guess = ""

    for letter in secret_word:
        if letter in letters_guessed:
            users_guess += letter
        else:
            users_guess += " _ "

    return users_guess


def get_available_letters(letters_guessed):
    avaliable_letters = string.ascii_lowercase

    for letter in letters_guessed:
        avaliable_letters = avaliable_letters.replace(letter, "")

    return avaliable_letters


def match_with_gaps(my_word, other_word):
    my_word_condensed = ""
    for letter in my_word:
        if letter != " ":
            my_word_condensed = my_word_condensed + letter        
    other_word = other_word.strip()

    if len(my_word_condensed) == len(other_word):
        for index in range(len(my_word_condensed)):
            if my_word_condensed[index] in string.ascii_lowercase:
                if my_word_condensed[index] != other_word[index]:
                    return False
            else:
                if other_word[index] in my_word_condensed:
                    return False
        else:
            return True
    else:
       return False


def show_possible_matches(my_word):
    matched_words = ""
    
    for word in wordlist:
        if match_with_gaps(my_word, word) == True:
            matched_words = matched_words + word + " "

    if len(matched_words) > 0:
        print(matched_words)
    else:
        print("No matches found.")

    return

def game(secret_word):
    guesses_remaining = 6
    letters_guessed = []
    vowels_list = ["a", "e", "i", "o", "u"]
    warnings_remaining = 3
    correct_guesses = 0
    image_sections = image_section_array(secret_word)
    file_name = choose_image(secret_word)
    
    print("Welcome to the Animal Guessing Game!")
    print("I am thinking of a word that is", len(secret_word), "letters long.")
    print("You have", guesses_remaining, "guesses left.")
    print("You have", warnings_remaining, "warnings left.")
    print("-------------")

    while guesses_remaining > 0:
        print("You have", guesses_remaining, "guesses left.")
        print("Available letters:", get_available_letters(letters_guessed))
        new_letter = input('Please guess a letter: ')
        new_letter = new_letter.lower()

        if new_letter == secret_word:
            correct_guesses = len(secret_word)
            show_image(file_name, image_sections, secret_word,
                       correct_guesses)
            print("Good guess:", secret_word)
            print("Congratulations, you won!")
            print("Your total score for this game is:", guesses_remaining * len(set(secret_word)))
            return

        elif new_letter not in string.ascii_lowercase:
            if new_letter == "*":
                show_possible_matches(get_guessed_word(secret_word, letters_guessed))
            else:
                warnings_remaining -= 1
                if warnings_remaining < 1:
                    guesses_remaining -= 1
                    print("Oops! You have no warnings left so you lose one guess:", get_guessed_word(secret_word, letters_guessed))
                    show_image(file_name, image_sections, secret_word,
                               correct_guesses)
                else:
                    print("Oops! That is not a valid letter. You have", warnings_remaining, "warnings left:", get_guessed_word(secret_word, letters_guessed))
                    show_image(file_name, image_sections, secret_word,
                               correct_guesses)
        elif new_letter in letters_guessed:
            warnings_remaining -= 1
            if warnings_remaining < 1:
                guesses_remaining -= 1
                print("Oops! You have no warnings left so you lose one guess:", get_guessed_word(secret_word, letters_guessed))
                show_image(file_name, image_sections, secret_word, correct_guesses)
            else:
                print("Oops! You've already guessed that letter. You have", warnings_remaining, "warnings left:", get_guessed_word(secret_word, letters_guessed))
                show_image(file_name, image_sections, secret_word,
                           correct_guesses)
        else:
            letters_guessed.append(new_letter)

            if new_letter in secret_word:
                correct_guesses = len(get_guessed_word(secret_word, letters_guessed).replace(" _ ", ""))
                print("Good guess:", get_guessed_word(secret_word, letters_guessed))
                show_image(file_name, image_sections, secret_word,
                           correct_guesses)

                if is_word_guessed(secret_word, letters_guessed) == True:
                    print("Congratulations, you won!")
                    print("Your total score for this game is:", guesses_remaining*len(set(secret_word)))
                    return
                            
            else:
                print("Oops! That letter is not in my word:", get_guessed_word(secret_word, letters_guessed))
                show_image(file_name, image_sections, secret_word,
                           correct_guesses)
                guesses_remaining -= 1
                if new_letter in vowels_list:
                    guesses_remaining -= 1
                
        print("-------------")
    print("Sorry, you ran out of guesses. The word was", secret_word, ".")
    correct_guesses = len(secret_word)
    show_image(file_name, image_sections, secret_word, correct_guesses)
    return


if __name__ == "__main__":
    secret_word = choose_word(wordlist)
    game(secret_word)
