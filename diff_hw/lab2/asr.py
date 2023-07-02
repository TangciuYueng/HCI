import threading
import webbrowser
import random
from difflib import SequenceMatcher
from PyQt5 import QtWidgets, QtGui, QtCore, uic
from PyQt5.QtWidgets import QPushButton, QMessageBox, QLabel, QCheckBox
from PyQt5.QtCore import Qt
import os
from asrInterface import Ui_MainWindow
import sys
import speech_recognition as sr

'''
compare two strings 
return the similarity as percent
'''
def similarityBetween(string1, string2):
    return SequenceMatcher(None, string1, string2).quick_ratio()

class myWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(myWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.myThread = None
    
    def showEvent(self, e):
        print("Window shows")
        try:
            self.recThread = RecognizeThread()
            '''
            设置守护线程，主线程结束了这个线程也死亡
            否则会出现关闭MainWindow但该线程中还在接受声音，而非立即关闭
            '''
            self.recThread.daemon = True
            self.recThread.start()
        except :
            print("Thread failed!")
            # close the Window
            self.close()
    
    def closeEvent(self, e):
        self.recThread.stop()
        print("Window closes")

    # 双击 or f1进入帮助界面
    def showDialog(self):
        print("dialog shows")
        QMessageBox.about(self, "help", "help list\n...")

    def mouseDoubleClickEvent(self, e):
        print("double click")
        self.showDialog()

    def keyPressEvent(self, e):
        print("press key")
        if e.key() == Qt.Key_F1:
            self.showDialog()


class RecognizeThread(threading.Thread):
    def __init__(self):
        super(RecognizeThread, self).__init__()
        self._loop = True
        self._lock = threading.Lock()
        self._op_list = ["music", "note", "baidu", "calculator"]
    
    def recognize_speech_from_mic(self, recognizer, microphone):
        """Transcribe speech from recorded from `microphone`.

        Returns a dictionary with three keys:
        "success": a boolean indicating whether or not the API request was
                   successful
        "error":   `None` if no error occured, otherwise a string containing
                   an error message if the API could not be reached or
                   speech was unrecognizable
        "transcription": `None` if speech could not be transcribed,
                   otherwise a string containing the transcribed text
        """
        # check that recognizer and microphone arguments are appropriate type
        if not isinstance(recognizer, sr.Recognizer):
            raise TypeError("`recognizer` must be `Recognizer` instance")

        if not isinstance(microphone, sr.Microphone):
            raise TypeError("`microphone` must be `Microphone` instance")

        # adjust the recognizer sensitivity to ambient noise and record audio
        # from the microphone
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        # set up the response object
        response = {
            "success": True,
            "error": None,
            "transcription": None
        }

        # try recognizing the speech in the recording
        # if a RequestError or UnknownValueError exception is caught,
        #     update the response object accordingly
        try:
            response["transcription"] = recognizer.recognize_sphinx(audio)
        except sr.RequestError:
            # API was unreachable or unresponsive
            response["success"] = False
            response["error"] = "API unavailable"
        except sr.UnknownValueError:
            # speech was unintelligible
            response["error"] = "Unable to recognize speech"

        return response

    # override the run()
    def run(self):
        recognizer = sr.Recognizer()
        microphone = sr.Microphone()
        while self._loop:
            res = self.recognize_speech_from_mic(recognizer, microphone)
            if res["error"]:
                print("ERROR: {}".format(res["error"]))
                continue
            cmd = res["transcription"]

            # 计算和每个功能的相似度
            similarity_list = []
            for op in self._op_list:
                similarity_list.append(similarityBetween(cmd, op))
            # 取最大的
            max_similarity = max(similarity_list)
            maxIdx = similarity_list.index(max_similarity)
            # 相似性实在太小，随机选一个
            if max_similarity < 0.25:
                maxIdx = random.randint(0, len(self._op_list) - 1)

            if self._op_list[maxIdx] == "music":
                print("music") 
                os.system("f1lcapae.wav")
            elif self._op_list[maxIdx] == "note":
                print("notepad")
                os.system("notepad")                    
            elif self._op_list[maxIdx] == "baidu":
                print("open Bilibili.com")
                webbrowser.open("https://bilibili.com")
            else:
                print("Calculator")
                os.system("f1lcapae.wav")

    def stop(self):
        self._lock.acquire()
        self._loop = False
        self._lock.release()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    application = myWindow()
    application.show()
    sys.exit(app.exec_())