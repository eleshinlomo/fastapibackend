#Importing Pytube library
import pytube
import requests

# Functions
from functions.whisper_speech_to_text import convert_audio_to_text

# Reading the above Taken movie Youtube link
videourl = 'https://www.youtube.com/watch?v=-LIIf7E-qFI'
one_mb = int(1024 * 1024)
max_file_size = 25

def convert_youtube_video_to_mp4(videourl):
    try:
        response = requests.head(videourl)
        get_video_size_in_bytes = response.headers.get('Content-Length')
        video_size_in_bytes = int(get_video_size_in_bytes)
        if video_size_in_bytes is not None:
            print(f'Video size is {int(video_size_in_bytes)} bytes')
            video_size_in_mb = video_size_in_bytes / one_mb
            print(f'{video_size_in_mb}MB')
        else:
            print("No filsize found in headers")
        

        data = pytube.YouTube(videourl)
        if data and video_size_in_mb <= max_file_size:
            # Converting and downloading as 'MP4' file
            audio = data.streams.get_audio_only()
            converted_audio_to_speech = convert_audio_to_text(audio)
            return converted_audio_to_speech
        
        else:
            raise Exception("Filesize is more than 25mb. Only lower files accepted")
    except Exception as e:
        return str(e)
        


result = convert_youtube_video_to_mp4(videourl)
print(result)