import logging
import keyboard
import os
import webbrowser
import sounddevice as sd

from RealtimeSTT import AudioToTextRecorder
from tts import speak

is_listening = False

def choose_microphone():

    devices = sd.query_devices()

    print("\n===================================")
    print(" Available Microphones ")
    print("===================================\n")

    available_mics = []

    for index, device in enumerate(devices):

        if device['max_input_channels'] > 0:

            print(f"{index}: {device['name']}")

            available_mics.append(index)

    while True:

        try:

            mic_index = int(input("\nEnter microphone index: "))

            if mic_index in available_mics:
                return mic_index

            else:
                print("Invalid microphone index")

        except ValueError:

            print("Please enter a valid number")


def start_listening():

    global is_listening

    is_listening = True

    print("\nListening started...\n")

    speak("Listening started")


def stop_listening():

    global is_listening

    is_listening = False

    print("\nListening stopped...\n")

    speak("Listening stopped")


def process_text(text):

    text = text.strip().lower()

    if len(text) < 2:
        return

    print(f"\nUser: {text}")

    if "open chrome" in text:

        speak("Opening Google Chrome")

        os.system("start chrome")

    elif "close chrome" in text:

        speak("Closing Google Chrome")

        os.system("taskkill /f /im chrome.exe")

    elif "open google" in text:

        speak("Opening Google")

        webbrowser.open("https://google.com")

    elif "close google" in text:

        speak("Closing Google")

        os.system("taskkill /f /im chrome.exe")

    elif "open youtube" in text:

        speak("Opening YouTube")

        webbrowser.open("https://youtube.com")

    elif "close youtube" in text:

        speak("Closing YouTube")

        os.system("taskkill /f /im chrome.exe")

    elif "open vs code" in text:

        speak("Opening Visual Studio Code")

        os.system("code")

    elif "close vs code" in text:

        speak("Closing Visual Studio Code")

        os.system("taskkill /f /im Code.exe")

    elif "start listening" in text:

        start_listening()

    elif "stop listening" in text:

        stop_listening()

    elif "exit assistant" in text:

        speak("Closing assistant")

        os._exit(0)

    else:

        speak(text)


def start_assistant():

    global is_listening

    print("Loading AI Voice Assistant...")

    mic_index = choose_microphone()

    recorder = AudioToTextRecorder(

        input_device_index=mic_index,

        model="small",

        language=None,

        compute_type="int8",

        spinner=False,

        level=logging.WARNING
    )

    keyboard.add_hotkey("F9", start_listening)

    keyboard.add_hotkey("F10", stop_listening)

    print("\n===================================")
    print(" Real-Time AI Voice Assistant ")
    print("===================================")

    print("F9  -> Start Listening")
    print("F10 -> Stop Listening")
    print("ESC -> Exit Assistant")

    print("\nWaiting for command...\n")

    while True:

        if keyboard.is_pressed("esc"):

            speak("Exiting assistant")

            break

        if is_listening:

            recorder.text(process_text)