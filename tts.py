import pyttsx3

def speak(text):

    try:
 
        print("Assistant:", text)

        engine = pyttsx3.init()

        engine.setProperty('rate', 150)

        engine.say(text)

        engine.runAndWait()

        engine.stop()

        del engine

    except Exception as e:

        print("TTS Error:", e)