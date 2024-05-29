import os
from dotenv import load_dotenv
from openai import OpenAI
import spacy

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


# Load the English language model
nlp = spacy.load("en_core_web_sm")

# LLM-generated message
llm_message = "Your LLM-generated message goes here."

# Process the LLM-generated message using spaCy
doc = nlp(llm_message)

# Convert spaCy Doc object to natural language (lemmatized tokens)
natural_language = " ".join([token.lemma_ for token in doc])

print(natural_language)
