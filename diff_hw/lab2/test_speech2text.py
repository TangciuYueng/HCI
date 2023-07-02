import speech_recognition as sr
import pyttsx3

r = sr.Recognizer()
with sr.Microphone() as source:
# with sr.AudioFile('E:\\xx\\HCI\\lab2\\f1lcapae.wav') as source:
    print('Say something')
    audio = r.listen(source)
try:
    text = r.recognize_google(audio)
    print('You said: ' + text)
    pyttsx3.speak('You said ' + text)
except sr.UnknownValueError:
    print('Don\'t understand')
except sr.RequestError as e:
    print('Could not request from G ' + format(e))
