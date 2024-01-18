import os
import json
import random

# Save messages for retrieval later on
def get_recent_messages():

  # Define the file name
  file_name = "stored_data.json"
  learn_instruction = {"role": "system", 
                       "content": """
                      You are a Sales Rep for a company called Fixupe. Your name is Bola. 
                      You are not only limited to answering questions about Fixupe. 
                      You should also answer general questions when asked. Be very flexible, playful,
                      chatty, funny, and keep great conversation 
                      full of unexpected gestures. Come up with things that can spark up 
                      good a good joke during conversation.
                      Fixupe is an 
                       IT company with focus on AI products. Our services include
                       1. Text to speech
                       2. Speech to text
                       3. Voice Chatbot
                       4. Voice Recorder (This is a free service)
                       5. AI Image Generator
                       6. AI Music Generator
                       7. AI Video Generator 
                       and lots more
                       . Keep responses under 20 words. Encourage them to provide 
                       you with the needs for their project 
                       as we are sure of providing a solution.
                       """
                       }
  
  # Initialize messages
  messages = []

  # Add Random Element
  x = random.uniform(0, 1)
  if x < 0.2:
    learn_instruction["content"] = learn_instruction["content"] + "Your response will have some light humour. "
  elif x < 0.5:
    learn_instruction["content"] = learn_instruction["content"] + "Your response will include an interesting new fact about Fixupe. "
  else:
    learn_instruction["content"] = learn_instruction["content"] + "Your response will recommend a service to check out of Fixupe. "

  # Append instruction to message
  messages.append(learn_instruction)

  # Get last messages
  try:
    with open(file_name) as user_file:
      data = json.load(user_file)
      
      # Append last 5 rows of data
      if data:
        if len(data) < 5:
          for item in data:
            messages.append(item)
        else:
          for item in data[-5:]:
            messages.append(item)
  except:
    pass

  
  # Return messages
  return messages


# Save messages for retrieval later on
def store_messages(message_decoded, chat_response):

  # Define the file name
  file_name = "stored_data.json"

  # Get recent messages
  messages = get_recent_messages()[1:]

  # Add messages to data
  user_message = {"role": "user", "content": message_decoded}
  assistant_message = {"role": "assistant", "content": chat_response}
  messages.append(user_message)
  messages.append(assistant_message)

  # Save the updated file
  with open(file_name, "w") as f:
    json.dump(messages, f)
  return


# Save messages for retrieval later on
def reset_messages():

  # Define the file name
  file_name = "stored_data.json"

  # Write an empty file
  open(file_name, "w")
  return
