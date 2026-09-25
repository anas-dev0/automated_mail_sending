import pandas as pd
import os
import json
import time
import random
from dotenv import load_dotenv
from langchain.messages import SystemMessage, HumanMessage

from prompt import create_prompt, create_relevance_check_prompt
from mail import send_email

load_dotenv()

SYSTEM_PROMPT = SystemMessage(content="""You are a professional email writer.
You MUST respond with valid JSON only — no preamble, no explanation, no markdown fences.
Your entire response must be a single JSON object.""")

RELEVANCE_CHECK_SYSTEM = "You are a classifier. You MUST respond with valid JSON only — no preamble, no explanation, no markdown fences."

CSV_FILE = os.getenv("LEADS_FILE", "leads.csv")
SUBJECT_COLUMN = os.getenv("CSV_SUBJECT_COLUMN", "subject")
COMPANY_COLUMN = os.getenv("CSV_COMPANY_COLUMN", "company")
EMAIL_COLUMN = os.getenv("CSV_EMAIL_COLUMN", "email")
START_ROW = int(os.getenv("START_ROW", "0"))
DELAY_MIN_SECONDS = float(os.getenv("EMAIL_DELAY_MIN_SECONDS", "240"))
DELAY_MAX_SECONDS = float(os.getenv("EMAIL_DELAY_MAX_SECONDS", "300"))

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "google").lower()


def build_llm():
    if LLM_PROVIDER == "google":
        from langchain_google_genai import ChatGoogleGenerativeAI
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise RuntimeError("GOOGLE_API_KEY must be set in your .env file when LLM_PROVIDER=google.")
        model = os.getenv("LLM_MODEL", "gemini-2.0-flash")
        return ChatGoogleGenerativeAI(model=model, temperature=0, api_key=api_key)
    elif LLM_PROVIDER == "ollama":
        from langchain_ollama import ChatOllama
        model = os.getenv("LLM_MODEL", "llama3.1")
        return ChatOllama(model=model, temperature=0)
    else:
        raise ValueError(f"Unsupported LLM_PROVIDER '{LLM_PROVIDER}'. Use 'google' or 'ollama'.")


def main():
    if not os.path.exists(CSV_FILE):
        raise FileNotFoundError(
            f"'{CSV_FILE}' not found. Copy 'leads.example.csv' to '{CSV_FILE}' and fill it in "
            f"with the companies/contacts you want to reach out to."
        )

    df = pd.read_csv(CSV_FILE)
    llm = build_llm()

    for index, row in df[START_ROW:].iterrows():
        subject_of_internship = row[SUBJECT_COLUMN]
        company = row[COMPANY_COLUMN]
        contact_email = row[EMAIL_COLUMN]

        relevance_check_prompt = create_relevance_check_prompt(sujet=subject_of_internship)
        relevant_response = llm.invoke([SystemMessage(content=RELEVANCE_CHECK_SYSTEM), HumanMessage(content=relevance_check_prompt)])
        try:
            relevance_result = json.loads(relevant_response.content)["related"]
        except (json.JSONDecodeError, KeyError, TypeError):
            print(f"Row {index} - Error parsing relevance check response")
            continue

        print(f"Row {index} - Relevance Check Result: {relevance_result}")
        if relevance_result.lower() != "yes":
            continue

        user_prompt = create_prompt(sujet=subject_of_internship, firm_name=company, email=contact_email)
        response = llm.invoke([SYSTEM_PROMPT, HumanMessage(content=user_prompt)])
        try:
            result = json.loads(response.content)
        except json.JSONDecodeError:
            print(f"Row {index} - Error parsing email generation response")
            continue

        print(result["subject"])
        print(result["body"])
        try:
            send_email(subject=result["subject"], body=result["body"], recepient=contact_email)
        except Exception as e:
            print(f"Error occurred while sending email for row {index}: {e}")
            continue

        time.sleep(random.uniform(DELAY_MIN_SECONDS, DELAY_MAX_SECONDS))
        print(index)


if __name__ == "__main__":
    main()
