import requests
import random
import speech_recognition as sr

def get_random_word():
    url = "https://random-word-api.herokuapp.com/word"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            word = response.json()[0]
            return word
        else:
            print("Couldn't retrieve random word. Ensure proper internet connection.")
            return None
    except Exception as e:
        print("Error", str(e))
        return None

def display_word(word, guessed_letters):
    result = ""
    for letter in word:
        if letter in guessed_letters:
            result += letter
        else:
            result += "_"
    return result

def get_guess():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak! Say a letter:")
        audio = recognizer.listen(source)

    try:
        guess = recognizer.recognize_google(audio)
        return guess.lower()
    except sr.UnknownValueError:
        print("Sorry I couldn't understand. Try again!")
        return None
    except sr.RequestError:
        print("There was an error with the speech recognition service. Try again!")
        return None

word_to_guess = get_random_word()  
guessed_letters = []
attempts = 6

while attempts > 0:
    print("Word: " + display_word(word_to_guess, guessed_letters))
    print("Attempts left: " + str(attempts))
    
    guess = get_guess()
    if guess:
        if len(guess) == 1 and guess.isalpha():
            if guess in guessed_letters:
                print("Try a different letter, you've already guessed this one!")
            elif guess in word_to_guess:
                guessed_letters.append(guess)
                print("Great job!")
            else:
                guessed_letters.append(guess)
                attempts -= 1
                print("Wrong guess!")
        else:
            print("Please say a single letter.")
    
    if word_to_guess == display_word(word_to_guess, guessed_letters):
        print("You win! The word was: " + word_to_guess)
        break

if attempts == 0:
    print("You're out of attempts. The word was: " + word_to_guess)