import pyttsx3
engine = pyttsx3.init()
engine.setProperty('rate', 200)
engine.setProperty('volume', 0.5)
engine.say("浓妆艳抹，把苏老师吃药，擦印度神油，大战三百回合")
engine.runAndWait()

# pyttsx3.speak("马威是我的神，苏老师是我的爱情")