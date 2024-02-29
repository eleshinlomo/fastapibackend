from dotenv import load_dotenv
import openai
from openai import OpenAI
import os
import requests


load_dotenv()

client = OpenAI()
    # This is the default and can be omitted
    # api_key=os.environ.get("OPENAI_API_KEY"),



BASE_URL = os.environ.get('BASE_URL')

#fetch sessionid
def fetch_sessionid(BASE_URL):
    try:
       headers = {
      'Content-Type': 'application/json'
        }
       response = requests.get(BASE_URL + '/fastapisessionidsender/', headers)
       if response:
            sessionid = response.json()
            return sessionid
       else:
          raise Exception('No response from credit server')
    except Exception as e:
       return str(e)

# Fetch Credit
async def fetch_credit():
   
  
    try:
        sessionid = fetch_sessionid()

        headers = {
        'Content-Type': 'application/json',
        'sessionid': sessionid
            }

        if sessionid:
           response = await requests.get(BASE_URL + '/getcredit/', headers)
           credit = response.json()
           return credit
        else:
            raise Exception('Sessionid not found')
    except Exception as e:
       return str(e)


# Image Generator
async def generate_image(payload:str, resolution):
  try:
    
    credit = await fetch_credit()

    if credit is not None and credit != 0:
        print(credit)
        response = client.images.generate(
        model="dall-e-3",
        prompt=payload,
        size=resolution,
        quality="hd",
        n=1,
        )

        image_url = response.data[0].url
        return image_url
    else:
        raise Exception('You do not have enough credit')
  except Exception as e:
     return str(e)

