from gtts import gTTS
import os

def text_to_speech(chat_response, language='en', output_file='output.mp3'):
  
    tts = gTTS(text=chat_response, lang=language, slow=False)
    tts.save(output_file)
    return output_file

    


