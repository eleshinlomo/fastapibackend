
from dotenv import load_dotenv
import os
import openai

load_dotenv()


# Retrieve Enviornment Variables
openai.organization = os.environ.get("OPEN_AI_ORG")
openai.api_key = os.environ.get("OPEN_AI_KEY")
# Convert audio to text
def elevenlabs_transcribe(audio_file):
  try:
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    message_text = transcript["text"]
    return message_text
  except Exception as e:
    return 