from dotenv import load_dotenv
import openai
from openai import OpenAI
import os


load_dotenv()

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)


def generate_image():
  response = client.image.generate(
    model="dall-e-3",
    prompt="a white siamese cat",
    size="1024x1024",
    quality="standard",
    n=1,
    )

  image_url = response.data[0].url
  return image_url

url= generate_image()
print(url)