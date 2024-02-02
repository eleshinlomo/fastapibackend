from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def openai_text_to_speech_converter(text, model, voice):
    try:
        # Generate audio speech from text
        response = client.audio.speech.create(
            model=model,
            voice=voice,
            input=text
        )

        # Check if the response contains audio data
        if 'audio' in response:
            audio_data = response['audio']
            with open("output.mp3", "wb") as audio_file:
                audio_file.write(audio_data)

            return audio_data
            return response['audio']

        # If 'audio' field is not present in the response, return None or handle it accordingly
        
        else:
            raise Exception("No audio found in response")

    except Exception as e:
        # Handle specific exceptions if needed
        print(e)
        return str(e)
