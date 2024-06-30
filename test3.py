import logging
import os
import time
from datetime import datetime

import speech_recognition as sr
from pydub import AudioSegment

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def listen_for_minute(duration):
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    logging.info("Adjusting for ambient noise... Please wait.")
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        logging.info("Listening for at least %d seconds...", duration)

        start_time = time.time()
        audio_data = []
        while True:
            if time.time() - start_time > duration:
                break
            try:
                logging.info("Listening...")
                audio_segment = recognizer.listen(source, timeout=10, phrase_time_limit=10)
                audio_data.append(audio_segment)
            except sr.WaitTimeoutError:
                logging.warning("Listening timeout, continuing...")
                continue

    logging.info("Finished listening.")
    return audio_data

def save_audio_segments(audio_data):
    combined = AudioSegment.empty()
    for i, segment in enumerate(audio_data):
        audio_file = f"audio_segment_{i}.wav"
        with open(audio_file, "wb") as f:
            f.write(segment.get_wav_data())
        combined += AudioSegment.from_wav(audio_file)
        os.remove(audio_file)  # Clean up the segment file after combining
    combined.export("combined_audio.wav", format="wav")
    return "combined_audio.wav"

def recognize_speech_from_audio_file(file_path, service='google'):
    recognizer = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio = recognizer.record(source)

    try:
        if service == 'google':
            text = recognizer.recognize_google(audio)
        elif service == 'sphinx':
            text = recognizer.recognize_sphinx(audio)
        # Add more services as needed
        else:
            raise ValueError("Unsupported recognition service specified.")
        return text
    except sr.UnknownValueError:
        logging.error("Speech Recognition could not understand the audio.")
    except sr.RequestError as e:
        logging.error(f"Could not request results from the Speech Recognition service; {e}")
    except Exception as e:
        logging.error(f"An error occurred during recognition: {e}")

    return ""

def main():
    d1 = datetime.now()
    print("Date-1: ", d1)
    try:
        audio_segments = listen_for_minute(60)
        audio_file = save_audio_segments(audio_segments)
        transcribed_text = recognize_speech_from_audio_file(audio_file, service="google")
        logging.info("Transcribed text: %s", transcribed_text)
    except KeyboardInterrupt:
        logging.info("Process interrupted by user.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    d2 = datetime.now()
    print("Date-2: ", d2)
    print("Diff d2-d1: ", d2 - d1)

if __name__ == "__main__":
    main()
