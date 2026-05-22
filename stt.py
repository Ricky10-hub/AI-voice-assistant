import os
import keyboard
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import webbrowser
import threading
import webrtcvad
from dotenv import load_dotenv
from groq import Groq
from tts import speak

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


SAMPLE_RATE = 16000
CHANNELS = 1
FRAME_DURATION = 20

is_listening = False


vad = webrtcvad.Vad(3)


devices = sd.query_devices()

mic_index = None

print("\nAvailable Microphones")
print("=" * 35)

for index, device in enumerate(devices):

    if device["max_input_channels"] > 0:

        print(f"{index}: {device['name']}")

        name = device["name"].lower()

        if (
            "headset" in name
            and "hands-free" not in name
        ):

            mic_index = index

if mic_index is None:

    mic_index = sd.default.device[0]

print(f"\nSelected microphone index: {mic_index}")


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


keyboard.add_hotkey("F9", start_listening)

keyboard.add_hotkey("F10", stop_listening)


def process_command(text):

    text = text.lower().strip()

    print(f"\nUser: {text}")

    if "open youtube" in text:

        speak("Opening YouTube")

        webbrowser.open("https://youtube.com")

    elif "close youtube" in text:

        speak("Closing YouTube tab")

        keyboard.press_and_release("ctrl+w")

    elif "open google" in text:

        speak("Opening Google")

        webbrowser.open("https://google.com")

    elif "close google" in text:

        speak("Closing Google tab")

        keyboard.press_and_release("ctrl+w")

    elif "open chrome" in text:

        speak("Opening Chrome")

        os.system("start chrome")

    elif "close chrome" in text:

        speak("Closing Chrome")

        os.system("taskkill /f /im chrome.exe")

    elif "open vs code" in text:

        speak("Opening Visual Studio Code")

        os.system("code")

    elif "close vs code" in text:

        speak("Closing Visual Studio Code")

        os.system("taskkill /f /im Code.exe")

    elif "exit assistant" in text:

        speak("Closing assistant")

        os._exit(0)

    else:

        speak(text)


def record_audio():

    print("Listening for speech...")

    frames = []

    silence_counter = 0

    block_size = int(SAMPLE_RATE * FRAME_DURATION / 1000)

    stream = sd.RawInputStream(
        samplerate=SAMPLE_RATE,
        blocksize=block_size,
        dtype='int16',
        channels=1,
        device=mic_index
    )

    with stream:

        while True:

            data, overflowed = stream.read(block_size)

            is_speech = vad.is_speech(
                data,
                SAMPLE_RATE
            )

            if is_speech:

                silence_counter = 0

                frames.append(data)

            else:

                silence_counter += 1

                if len(frames) > 0:

                    frames.append(data)

            if silence_counter > 8 and len(frames) > 0:

                break

    return b''.join(frames)

def listen_loop():

    global is_listening

    while True:

        try:

            if is_listening:

                audio_bytes = record_audio()

                audio_np = np.frombuffer(
                    audio_bytes,
                    dtype=np.int16
                )

                wav.write(
                    "temp.wav",
                    SAMPLE_RATE,
                    audio_np
                )

                print("Transcribing with Groq...")

                with open("temp.wav", "rb") as file:

                    transcription = client.audio.transcriptions.create(

                        file=file,

                        model="whisper-large-v3-turbo",

                        response_format="json"
                    )

                text = transcription.text.strip()

                if len(text) > 1:

                    process_command(text)

                else:

                    print("No speech detected")

        except Exception as e:

            print("Error:", e)

print("\n===================================")
print(" Real-Time AI Voice Assistant ")
print("===================================")

print("\nF9  -> Start Listening")
print("F10 -> Stop Listening")
print("ESC -> Exit Assistant")

print("\nWaiting for command...\n")

thread = threading.Thread(target=listen_loop)

thread.daemon = True

thread.start()

keyboard.wait("esc")

print("\nAssistant closed")