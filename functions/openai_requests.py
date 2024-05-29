from openai import OpenAI
import os

# Document libraries
# import docx
import os
from dotenv import load_dotenv
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import BaseOutputParser
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter



load_dotenv()
llm = ChatOpenAI( model_name="gpt-3.5-turbo", temperature=0.2, max_tokens=100)




enoch_url = 'https://fixupe.com/code'
# Prompt 
def handle_prompts():
    
    template = f"""
             
             Your name is Bola. Bola is pronounced as 'balla' 
             You are pretty much open to chatting about 
             anything. Keep your responses short. Don't be rigid, 
             be very flexible and flow with the chat. 
        
                """
    prompt = ChatPromptTemplate(
        messages=[
        SystemMessagePromptTemplate.from_template(template=template),
        # The `variable_name` here is what must align with memory
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template("{question}")
        ]
        )
    return prompt
    
        
def run_conversation(prompt, memory):
    conversation = LLMChain(
                llm=llm,
                prompt=prompt,
                verbose=False,
                memory=memory
                )
    return conversation
        
       
# Get Response
def get_chat_response(user_input):
    try:

        if user_input:
            prompt = handle_prompts()
            memory = ConversationBufferWindowMemory(memory_key="chat_history", return_messages=True, k=4)
            conversation = run_conversation(prompt, memory)
            response = conversation.run(question = user_input)
            return response
        else:
            raise Exception("Error with the data sent")
        
    except Exception as e:
        print(str(e))
        return str(e)
        




    



