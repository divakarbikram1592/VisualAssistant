from os import walk
import threading

import face_recognition
import cv2
import numpy as np

from Listening import Listening

class FaceApp:

    def playCamera(self):
        video_capture = cv2.VideoCapture(0)
        video_capture.set(3, 640)  # Width
        video_capture.set(4, 480)  # Height

        mypath = "/Users/apple/Documents/Projects-Test/pythonProject/RandomTestApp/source/resoures/faces/"
        filenames = next(walk(mypath), (None, None, []))[2]  # [] if no file
        known_face_encodings = []
        known_face_names = []
        for filename in filenames:
            try:
                sample_image_1 = face_recognition.load_image_file(mypath + "" + filename)
                sample_image_1_encoding = face_recognition.face_encodings(sample_image_1)[0]
                known_face_encodings.append(sample_image_1_encoding)
                known_face_names.append(filename.split(".")[0])
            except:
                print("")

        # Initialize some variables
        face_locations = []
        face_encodings = []
        face_names = []
        process_this_frame = True

        # initiate dialog
        objListening = Listening()
        objListening.init()

        prev_name = ""

        while True:
            ret, frame = video_capture.read()

            if process_this_frame:
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

                rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

                # Find all the faces and face encodings in the current frame of video
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                face_names = []
                for face_encoding in face_encodings:

                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                    name = "Unknown"

                    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = known_face_names[best_match_index]

                    face_names.append(name)

            process_this_frame = not process_this_frame

            for (top, right, bottom, left), name in zip(face_locations, face_names):
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            #############################################################
            ######################Other code#############################

            # if prev_name != name:
            #     prev_name = name
            #     objListening.updateName(prev_name)

            cv2.imshow('Video', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            #############################################################
            #############################################################

        # Release handle to the webcam
        video_capture.release()
        cv2.destroyAllWindows()

    def init(self):
        self.playCamera()