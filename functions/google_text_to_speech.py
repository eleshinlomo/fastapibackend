from gtts import gTTS
import os

def google_text_to_speech_converter(chat_response, language='en', output_file='output.mp3'):
  try:
    tts = gTTS(text=chat_response, lang=language, slow=False)
    tts.save(output_file)
    return output_file
  except Exception as e:
    return str(e)


    


