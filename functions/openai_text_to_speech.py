from pathlib import Path
from openai import OpenAI
client = OpenAI()
from starlette.responses import StreamingResponse


async def openai_text_to_speech_converter(text):
    try:
        response = await client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=text
        )

        async def audio_stream():
            async for chunk in response.aiter_content(chunk_size=1024):
                yield chunk
        
        return StreamingResponse(audio_stream(), media_type="audio/mpeg")
    
    except Exception as e:
        return None

