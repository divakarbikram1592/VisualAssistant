import threading
import time

import speech_recognition as sr
from QuestionAnswerDB import QuestionAnswerDB
import pygame

class Listening:

    name = ""

    def play_notification_sound(self):
        pygame.mixer.init()
        notification_sound = pygame.mixer.Sound("/Users/apple/Documents/Projects-Test/pythonProject/RandomTestApp/source/resoures/notification2.wav")
        notification_sound.play()

    def convertSpeechToText(self):
        r = sr.Recognizer()

        # Use the default microphone as the audio source
        with sr.Microphone() as source:
            # adjust microphone sensitivity to ambient noise
            r.adjust_for_ambient_noise(source)
            # continuously listen for audio input
            isPlayNotif = True
            while True:
                if isPlayNotif:
                    self.play_notification_sound()
                print("Say something!")
                audio = r.listen(source)

                try:
                    # recognize speech using Google Speech Recognition
                    text = r.recognize_google(audio)
                    print("You said:", text)
                    objQADb = QuestionAnswerDB()
                    objQADb.init(text, self.name)
                    time.sleep(5)
                    print("===>"+text)
                    if text == "":
                        isPlayNotif = False
                    else:
                        isPlayNotif = True

                    # Wait for some time before stopping the inner thread
                    # time.sleep(5)

                except sr.UnknownValueError:
                    isPlayNotif = False
                    print("Google Speech Recognition could not understand audio")

                except sr.RequestError as e:
                    isPlayNotif = False
                    print("Could not request results from Google Speech Recognition service; {0}".format(e))
            # # Listen for audio input
            # audio = r.listen(source)
            #
            # try:
            #     text = r.recognize_google(audio)
            #     print("You said:", text)
            #     objQADb = QuestionAnswerDB()
            #     objQADb.init(text)
            # except sr.UnknownValueError:
            #     print("Could not understand audio")
            # except sr.RequestError as e:
            #     print("Could not request results from Google Speech Recognition service; {0}".format(e))

            # try:
            #     # Use Google Speech Recognition to convert audio to text
            #     text = r.recognize_google(audio)
            #
            #     # Print the transcribed text
            #     return text
            # except sr.UnknownValueError:
            #     return "UnknownValueError"
            # except sr.RequestError as e:
            #     return "RequestError"

    def startSpeechToText(self):
        # print("tt")
        # self.convertSpeechToText()
        t1 = threading.Thread(target=self.convertSpeechToText, name='t1')
        t1.start()
        # t1.join()
        # result = self.convertSpeechToText()
        # print("======>", result)
        # if result == "UnknownValueError":
        #     print("Sorry, could not understand audio.")
        # elif result == "RequestError":
        #     print("Could not request results from Google Speech Recognition service")
        # else:
        #     print("You said: {}".format(result))

            # objQADb = QuestionAnswerDB()
            # objQADb.init(result)

    def updateName(self, name):
        self.name = name

    def init(self):
        # print("init")
        self.startSpeechToText()
        # while True:
        #     self.startSpeechToText()
