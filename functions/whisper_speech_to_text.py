
import openai

import os
import openai
from dotenv import load_dotenv

load_dotenv()

# Open AI - Whisper
# Convert audio to text
def convert_audio_to_text(audio_input):
  try:
    transcript = openai.Audio.transcribe("whisper-1", audio_input)
    message_text = transcript["text"]
    return message_text
  except Exception as e:
    return
