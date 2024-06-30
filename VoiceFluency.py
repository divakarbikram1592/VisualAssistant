import speech_recognition as sr
from pydub import AudioSegment
import numpy as np
from scipy.io import wavfile
from scipy.signal import find_peaks
import librosa


def analyze_speech(file_path):
    # Load audio file
    audio = AudioSegment.from_file(file_path)
    audio.export("temp.wav", format="wav")  # Convert to wav format for processing

    # Read the wav file
    rate, data = wavfile.read("temp.wav")

    # Initialize recognizer
    recognizer = sr.Recognizer()

    # Load the audio file into the recognizer
    with sr.AudioFile("temp.wav") as source:
        audio_data = recognizer.record(source)

    # Recognize speech using Google Web Speech API
    try:
        text = recognizer.recognize_google(audio_data)
        print("Recognized Text: ", text)
    except sr.UnknownValueError:
        print("Google Web Speech API could not understand the audio")
        return
    except sr.RequestError as e:
        print(f"Could not request results from Google Web Speech API; {e}")
        return

    # Analyze the audio data for fluency metrics
    analyze_fluency(data, rate, text, "temp.wav")


def analyze_fluency(data, rate, text, wav_path):
    # Convert to mono if stereo
    if len(data.shape) > 1:
        data = data.mean(axis=1)

    # Normalize audio data
    data = data / np.max(np.abs(data))

    # Compute the time between pauses
    silence_threshold = 0.02
    min_silence_duration = 0.3  # Minimum duration of silence to be considered a pause
    pauses = []
    current_pause_length = 0
    speaking_duration = 0

    for sample in data:
        if abs(sample) < silence_threshold:
            current_pause_length += 1
        else:
            speaking_duration += 1
            if current_pause_length >= min_silence_duration * rate:
                pauses.append(current_pause_length / rate)
            current_pause_length = 0

    # Compute speech rate (words per minute)
    total_time = len(data) / rate
    words = text.split()
    word_count = len(words)
    speech_rate = (word_count / total_time) * 60  # words per minute

    # Compute articulation rate (excluding pauses)
    speaking_duration_seconds = speaking_duration / rate
    articulation_rate = (word_count / speaking_duration_seconds) * 60  # words per minute

    # Compute phonation time ratio
    phonation_time_ratio = speaking_duration_seconds / total_time

    # Detect filler words
    filler_words = ['um', 'uh', 'like', 'so', 'you know']
    filler_count = sum(text.lower().count(filler) for filler in filler_words)

    # Compute jitter (frequency variation) and shimmer (amplitude variation)
    jitter = np.mean(np.abs(np.diff(data)))  # Simplistic jitter calculation
    shimmer = np.std(data) / np.mean(data)  # Simplistic shimmer calculation

    # Compute average speech intensity
    speech_intensity = np.mean(np.abs(data))

    # Estimate syllable count
    syllable_count = estimate_syllable_count(text)
    syllables_per_second = syllable_count / speaking_duration_seconds

    # Analyze prosody (pitch variation) using librosa
    y, sr = librosa.load(wav_path)
    pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
    pitch_values = pitches[pitches > 0]
    mean_pitch = np.mean(pitch_values)
    std_pitch = np.std(pitch_values)

    # Detect voice breaks
    peaks, _ = find_peaks(data, height=silence_threshold)
    voice_breaks = len(peaks)

    # Output the fluency metrics
    print(f"Total Time: {total_time:.2f} seconds")
    print(f"Word Count: {word_count}")
    print(f"Speech Rate: {speech_rate:.2f} words per minute")
    print(f"Articulation Rate: {articulation_rate:.2f} words per minute")
    print(f"Phonation Time Ratio: {phonation_time_ratio:.2f}")
    print(f"Number of Pauses: {len(pauses)}")
    print(f"Average Pause Duration: {np.mean(pauses):.2f} seconds")
    print(f"Filler Words Count: {filler_count}")
    print(f"Jitter: {jitter:.2f}")
    print(f"Shimmer: {shimmer:.2f}")
    print(f"Average Speech Intensity: {speech_intensity:.2f}")
    print(f"Syllable Count: {syllable_count}")
    print(f"Syllables per Second: {syllables_per_second:.2f}")
    print(f"Mean Pitch: {mean_pitch:.2f} Hz")
    print(f"Pitch Variation (Standard Deviation): {std_pitch:.2f} Hz")
    print(f"Voice Breaks: {voice_breaks}")


def estimate_syllable_count(text):
    vowels = "aeiouy"
    text = text.lower()
    count = 0
    for word in text.split():
        word_count = 0
        if word[0] in vowels:
            word_count += 1
        for index in range(1, len(word)):
            if word[index] in vowels and word[index - 1] not in vowels:
                word_count += 1
        if word.endswith("e"):
            word_count -= 1
        if word_count == 0:
            word_count += 1
        count += word_count
    return count


# Example usage
analyze_speech("/Users/apple/Documents/Project-Docker/VisualAssistant/combined_audio.wav")
