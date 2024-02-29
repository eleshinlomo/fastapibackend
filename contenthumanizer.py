import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()


def content_to_generate(prompt: str):
 try:
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
    {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
    {"role": "user", "content": prompt}
    ]
    )

    result = (completion.choices[0].message.content)
    print(result)
 except Exception as e:
   return str(e)

prompt = "Compose a poem that explains the concept of recursion javascript."
result = content_to_generate(prompt)