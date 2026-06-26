def create_prompt(firm_name, sujet, email):
    user_prompt = f"""Write a professional internship application email to {firm_name} for a {sujet} internship position, addressed to {email}.

The email must include:
- A polite greeting
- A brief introduction of the applicant (Anas Aouini, ICT Engineering Student at Sup'Com)
- A clear statement of interest in the internship
- A summary of relevant skills and experiences (see CV below)
- A note that the CV is attached
- A polite closing
- Maximum 200 words

--- CV ---
Anas Aouini | anas.aouini@supcom.tn | +216 58 934 007
ICT Engineering Student at Sup'Com (2nd year, focus: Telecom, AI, Software Engineering)
Ranked 86/1750 in preparatory cycle (Math-Physics)

Experience: Summer intern at TalentLink (Django + React University Management Platform)
Leadership: IEEE Sup'Com CS Chapter Chairperson

Key Projects:
- Jobify: real-time voice interview agent (LiveKit, Google Realtime API)
- Mealy: AI cooking app (Flutter, Flask, Firebase, food photo recognition)
- IndabaX Tunisia 2025 Website (Technical Manager)

Awards:
- 1st Place, Orange AI Hackathon (Churn prediction model)
- 2nd Place, CSTAM 2.0 (chatbot + nutrition-facts from food photos)

Skills: Python, C++, TypeScript, React, FastAPI, LangChain, PyTorch, Docker
Certifications: ML Specialization (Coursera), CCNA 1, Nvidia Deep Learning & Data Science
Languages: Arabic, English, French (all fluent)
--- END CV ---

Respond with ONLY this JSON structure, nothing else:
{{"subject": "...", "body": "..."}}"""

    return user_prompt