# Automated Internship/Job Application Emailer

Automatically emails a list of companies with a personalized application email
(written by an LLM) and your CV attached, filtering out leads that don't match
your field of interest first.

Given a CSV of leads (company, contact email, role/subject), this tool:

1. Asks an LLM whether each row is relevant to the fields you care about.
2. If relevant, asks the LLM to write a short, personalized application email
   using your profile/CV summary.
3. Sends the email (with your CV attached) to the contact and waits a random
   delay before moving to the next row, to avoid looking like spam.

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

If you want to use a local/self-hosted model via [Ollama](https://ollama.com)
instead of Google Gemini, also install and run Ollama, and pull a model.

### 2. Configure your `.env`

```bash
cp .env.example .env
```

Then edit `.env`:

- `EMAIL_ADDRESS` / `EMAIL_APP_PASSWORD` — the account you'll send from.
  `EMAIL_APP_PASSWORD` is **not** your normal password — it's an app-specific
  password. For a Microsoft/Outlook account, generate one under
  **Microsoft Account -> Security -> Advanced security options -> App
  passwords**. For Gmail, see **Google Account -> Security -> App passwords**
  (and update `SMTP_SERVER`/`SMTP_PORT` to `smtp.gmail.com` / `587`).
- `GOOGLE_API_KEY` — a Gemini API key from https://aistudio.google.com/apikey
  (only needed if `LLM_PROVIDER=google`, the default).
- `CANDIDATE_NAME`, `CV_FILE`, `PROFILE_FILE` — see below.

See the comments in `.env.example` for every other optional setting
(relevance topics, sending pace, CSV column names, etc.).

### 3. Add your CV and profile

- Put your CV PDF in the project folder and point `CV_FILE` at it (defaults
  to `cv.pdf`). It gets attached to every email.
- Copy `profile.example.txt` to `profile.txt` (the default `PROFILE_FILE`)
  and rewrite it with your own background: name, contact info, education,
  experience, projects, skills, etc. This is the text the LLM uses to write
  each email, so the more concrete and specific it is, the better the
  generated emails will be.

### 4. Add your leads

Copy `leads.example.csv` to `leads.csv` (the default `LEADS_FILE`) and fill
it in with the companies you want to reach out to. It needs three columns:

| subject | company | email |
|---|---|---|
| Backend Development Internship | Acme Corp | recruiting@acme-corp.example |

If your source spreadsheet uses different column names, either rename the
columns in your CSV, or point `CSV_SUBJECT_COLUMN` / `CSV_COMPANY_COLUMN` /
`CSV_EMAIL_COLUMN` in `.env` at your own column names.

> `data.ipynb` is an optional example notebook showing how the original
> dataset (a French-language internship-listing export) was filtered down
> to relevant rows before being saved as a leads CSV. It's a
> reference/starting point, not something the app depends on — adapt or
> ignore it based on how your own raw data looks.

### 5. Run it

```bash
python automatedapp.py
```

It will go through `leads.csv` from `START_ROW` onward (default `0`),
skipping irrelevant rows, sending an email for each relevant one, and
printing its progress (including the row index) as it goes. If it stops
partway through (rate limit, network error, etc.), note the last row index
it printed and set `START_ROW` to that value in `.env` to resume.

## Notes

- Sending automated emails to real people has ethical and legal
  implications (spam laws, a company's application process, etc.). Use this
  responsibly, personalize/verify what gets sent, and don't blast the same
  message at scale.
- `.env`, `profile.txt`, `cv.pdf`, and `leads.csv` are all gitignored since
  they contain your personal data — never commit them.
