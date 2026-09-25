import os

DEFAULT_PROFILE_PATH = os.getenv("PROFILE_FILE", "profile.txt")
DEFAULT_RELEVANCE_TOPICS = "AI, Machine Learning, Data Science, Deep Learning, NLP, Computer Vision"
DEFAULT_MAX_WORDS = "200"


def _load_profile(profile_path=DEFAULT_PROFILE_PATH):
    if not os.path.exists(profile_path):
        raise FileNotFoundError(
            f"Profile file '{profile_path}' not found. Copy 'profile.example.txt' to "
            f"'{profile_path}' and fill it in with your own background/CV summary."
        )
    with open(profile_path, "r", encoding="utf-8") as f:
        return f.read().strip()


def create_prompt(firm_name, sujet, email):
    candidate_name = os.getenv("CANDIDATE_NAME", "Your Name")
    max_words = os.getenv("MAX_EMAIL_WORDS", DEFAULT_MAX_WORDS)
    profile = _load_profile()

    user_prompt = f"""Write a professional internship application email to {firm_name} for a {sujet} internship position, addressed to {email}.

The email must include:
- A polite greeting
- A brief introduction of the applicant ({candidate_name})
- A clear statement of interest in the internship
- A summary of relevant skills and experiences (see profile below)
- A note that the CV is attached
- A polite closing
- Maximum {max_words} words

--- CANDIDATE PROFILE ---
{profile}
--- END CANDIDATE PROFILE ---

Respond with ONLY this JSON structure, nothing else:
{{"subject": "...", "body": "..."}}"""

    return user_prompt


def create_relevance_check_prompt(sujet):
    topics = os.getenv("RELEVANCE_TOPICS", DEFAULT_RELEVANCE_TOPICS)
    RELEVANCE_CHECK_USER = f"""Does this internship subject relate to any of the following fields: {topics}?
    Internship subject: {sujet}

    Respond with ONLY this JSON:
    {{"related": "yes"}} or {{"related": "no"}}"""
    return RELEVANCE_CHECK_USER
