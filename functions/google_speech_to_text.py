import io
import speech_recognition as sr
from pydub import AudioSegment

def speech_to_text(audio_input,  language='en-US'):
    recognizer = sr.Recognizer()

    try:
        # # Convert the SpooledTemporaryFile to a BytesIO object
        # audio_data = io.BytesIO(audio_input.read())

        # Load audio file using pydub
        audio = AudioSegment.from_file(audio_input)
        

        # Export audio as WAV (a common format)
        wav_data = io.BytesIO()
        audio.export(wav_data, format="wav")

        # Use AudioFile to create an AudioData object
        with sr.AudioFile(wav_data) as source:
            audio_data = recognizer.record(source)

        # Using Google Web Speech API for speech recognition
        text = recognizer.recognize_google(audio_data, language=language)
        return text
    except sr.UnknownValueError:
        print("Google Web Speech API could not understand the audio")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Google Web Speech API; {e}")
        return None