import threading
from gtts import gTTS
from io import BytesIO
import pygame

class Speaking:

    def play_sound(self, text):
        # Create the audio file in memory using gTTS
        tts = gTTS(text=text, lang='en')
        audio = BytesIO()
        tts.write_to_fp(audio)
        audio.seek(0)

        # Play the audio in memory using pygame mixer
        pygame.mixer.init()
        sound = pygame.mixer.Sound(audio)
        sound.play()

    def speak(self, text):
        # Create a new thread to play the sound asynchronously
        sound_thread = threading.Thread(target=self.play_sound, args=(text,))
        sound_thread.start()

    # Example usage:
    # speak("Hello, world!")

