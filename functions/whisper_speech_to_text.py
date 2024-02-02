
import os
import openai
from openai import OpenAI
from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)




# Open AI - Whisper
# Convert audio to text
def convert_audio_to_text(audio_data):
   try:
      transcript = client.audio.translations.create(
      model="whisper-1", 
      file=audio_data,
      )

      text = transcript.text
      return text
   except Exception as e:
      return str(e)
  


