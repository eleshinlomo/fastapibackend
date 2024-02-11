from dotenv import load_dotenv
import openai
from openai import OpenAI
import os


load_dotenv()

client = OpenAI()
    # This is the default and can be omitted
    # api_key=os.environ.get("OPENAI_API_KEY"),



def generate_image(payload:str, resolution):
  try:
      response = client.images.generate(
      model="dall-e-3",
      prompt=payload,
      size=resolution,
      quality="standard",
      n=1,
      )

      image_url = response.data[0].url
      return image_url
  except Exception as e:
     return str(e)

