from pocketsphinx import LiveSpeech
import pyaudio
import wave
import requests
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

def record_audio(file_path, duration=5):
    chunk = 1024
    format = pyaudio.paInt16
    channels = 1
    rate = 16000

    p = pyaudio.PyAudio()

    stream = p.open(format=format,
                    channels=channels,
                    rate=rate,
                    input=True,
                    frames_per_buffer=chunk)

    frames = []

    print("Recording...")

    for i in range(int(rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)

    print("Recording complete.")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(file_path, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(pyaudio.PyAudio().get_sample_size(format))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()

def recognize_speech(file_path):
    speech = LiveSpeech()

    print("Say a letter:")

    recognized_text = ""

    for phrase in speech:
        recognized_text += str(phrase)

    return recognized_text.lower()

word_to_guess = get_random_word()
guessed_letters = []
attempts = 5  # incorrect attempts allowed

while attempts > 0:
    print("Word: " + display_word(word_to_guess, guessed_letters))
    print("Attempts left: " + str(attempts))

    # Record audio and recognize speech
    audio_file_path = "recorded_audio.wav"
    record_audio(audio_file_path)
    guess = recognize_speech(audio_file_path)

    if guess:
        if len(guess) == 1 and guess.isalpha():
            if guess in guessed_letters:
                print("You've already guessed this letter.")
            elif guess in word_to_guess:
                guessed_letters.append(guess)
                print("Good guess!")
            else:
                guessed_letters.append(guess)
                attempts -= 1
                print("Incorrect guess!")
        else:
            print("Please say a single letter.")

    if word_to_guess == display_word(word_to_guess, guessed_letters):
        print("Congratulations, you've won! The word is " + word_to_guess)
        break

if attempts == 0:
    print("You've run out of attempts. The word was " + word_to_guess)
