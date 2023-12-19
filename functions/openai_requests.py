import os
import openai
from dotenv import load_dotenv
from functions.database import get_recent_messages

load_dotenv()


# Retrieve Enviornment Variables
openai.organization = os.environ.get("OPEN_AI_ORG")
openai.api_key = os.environ.get("OPEN_AI_KEY")


# Open AI - Whisper
# Convert audio to text
def convert_audio_to_text(audio_file):
  try:
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    message_text = transcript["text"]
    return message_text
  except Exception as e:
    return 



# Open AI - Chat GPT
# Convert audio to text
def get_chat_response(decoded_message):
    messages = get_recent_messages()
    user_message = {"role": "user", "content": decoded_message}
    messages.append(user_message)

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        message_text = response["choices"][0]["message"]["content"]

        # Check if the type is a string before returning
        if isinstance(message_text, str):
            return message_text
        else:
            return {"error": "Unexpected response type"}

    except Exception as e:
        return 
