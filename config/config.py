from dotenv import load_dotenv
import os

load_dotenv()


#######################################################
# GEMINI
#######################################################

API_KEYS = []

for i in range(1, 11):

    key = os.getenv(f"GEMINI_API_KEY_{i}")

    if key and key.strip():
        API_KEYS.append(key.strip())


MODEL_NAME = os.getenv(
    "MODEL_NAME",
    "gemini-2.5-flash"
)

#######################################################
# Gmail
#######################################################

GMAIL_EMAIL = os.getenv("GMAIL_EMAIL")

GMAIL_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")


#######################################################
# Retry
#######################################################

MAX_RETRIES = int(
    os.getenv(
        "MAX_RETRIES",
        "5"
    )
)

#######################################################
# Limits
#######################################################

EMAILS_PER_RUN = int(
    os.getenv(
        "EMAILS_PER_RUN",
        "100"
    )
)

#######################################################
# Files
#######################################################

from pathlib import Path

# Project Root
BASE_DIR = Path(__file__).resolve().parent.parent

# Files
COMPANY_FILE = BASE_DIR / "data" / "companies.xlsx"

OUTPUT_FILE = BASE_DIR / "data" / "generated_emails.xlsx"

CHECKPOINT_FILE = BASE_DIR / "data" / "checkpoint.json"

LOG_FILE = BASE_DIR / "logs" / "bot.log"

PROMPT_FILE = BASE_DIR / "prompts" / "internship_prompt.txt"

RESUME_PATH = BASE_DIR / "data" / "resume.pdf"

#######################################################
# Candidate Details
#######################################################

CANDIDATE = {

    "name": "XXX KUMAR",

    "college": "IIT JApan",

    "degree": "B.Tech",

    "batch": "2027",

    "roles": [

        "AI Developer",

        "Machine Learning Developer",

        "Data Analyst",

        "Data Engineer"

    ],

    "skills": [

        "Python",

        "C++",

        "SQL", "MongoDB"

        "Machine Learning",

        "Deep Learning",

        "Pandas",

        "NumPy", "DataBricks",

        "Scikit-learn",

        "TensorFlow",

        "PyTorch",

        "Power BI",

        "AWS",

        "PySpark",

        "Apache Kafka",

        "Data Engineering",

        "RAG",

        "LLMs",

        "Git"

    ],

    "projects": [

        "RAG Chatbot",

        "Stock Market Prediction using LSTM",

        "AWS YouTube Data Engineering Pipeline",

        "AI based ATS system",

        "Automatic mailing agent based on company (tailoring every email)"

    ]

}
