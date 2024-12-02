import speech_recognition as sr
import pyttsx3

recognizer = sr.Recognizer()
engine = pyttsx3.init()


def speak(text):
    engine.say(text)
    engine.runAndWait()

while True:
    try:
        with sr.Microphone() as mic:
            
            recognizer.adjust_for_ambient_noise(mic,duration=0.7)
            print("Listening")
            audio = recognizer.listen(mic)
            

            text = recognizer.recognize_google(audio)
            text = text.lower()

            print("Recognized :\n", text)

            speak(text)
    except sr.UnknownValueError :
        print("that was not  understood")
    except sr.RequestError as e:
        print("There has been a request error, results :",e)
    