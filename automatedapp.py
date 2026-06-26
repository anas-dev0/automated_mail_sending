import pandas as pd
import os
from dotenv import load_dotenv
from prompt import create_prompt
# from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama
from langchain.messages import SystemMessage, HumanMessage
import json
from mail import send_email
import time
import random

system_prompt = SystemMessage(content="""You are a professional email writer. 
You MUST respond with valid JSON only — no preamble, no explanation, no markdown fences.
Your entire response must be a single JSON object.""")


load_dotenv()
df = pd.read_csv('stage_fixed.csv')




# llm = ChatGoogleGenerativeAI(model="gemini-3-flash-preview", temperature=0 , api_key=os.getenv("google_api_key"))
llm = ChatOllama(model="gpt-oss:120b-cloud", temperature=0 )


for index, row in df[28::].iterrows():
    user_prompt = create_prompt(sujet =row['Sujet de stage'] , firm_name = row['Nom de la Société de stage'] , email = row["E-mail de contact pour votre encadrant/responsable de la société"])
    response = llm.invoke([system_prompt, HumanMessage(content=user_prompt)])
    result = json.loads(response.content)
    print(result["subject"])
    print (result["body"])
    send_email(subject=result["subject"], body=result["body"], recepient=row["E-mail de contact pour votre encadrant/responsable de la société"])
    time.sleep(random.uniform(50, 90))
    print(index)
    