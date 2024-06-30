import speech_recognition as sr
import time
from datetime import datetime

def listen_for_minute():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    print("Adjusting for ambient noise... Please wait.")
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening for at least one minute...")

        start_time = time.time()
        audio_data = []

        while True:
            if time.time() - start_time > 60:  # Check if one minute has passed
                break

            try:
                audio_segment = recognizer.listen(source, timeout=10, phrase_time_limit=10)
                audio_data.append(audio_segment)
            except sr.WaitTimeoutError:
                print("Listening timeout, continuing...")
                continue

        print("Finished listening.")

    return audio_data

def recognize_speech_from_audio(audio_data):
    recognizer = sr.Recognizer()
    complete_text = ""

    for audio_segment in audio_data:
        try:
            text = recognizer.recognize_google(audio_segment)
            complete_text += text + " "
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand the audio segment.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")

    return complete_text.strip()

# Main script
d1 = datetime.now()
print("Date-1: ", d1)
audio_segments = listen_for_minute()
d2 = datetime.now()
print("Date-2: ", d2)
print("Diff d2-d1: ", d2 - d1)
transcribed_text = recognize_speech_from_audio(audio_segments)
d3 = datetime.now()
print("Date-3: ", d3)
print("Diff d3-d2: ", d3 - d2)

print("Transcribed text:", transcribed_text)
d4 = datetime.now()
print("Date-4: ", d4)
print("Diff d4-d3: ", d4 - d3)
