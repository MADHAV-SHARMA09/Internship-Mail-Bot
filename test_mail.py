import smtplib
import ssl
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("GMAIL_EMAIL")
PASSWORD = os.getenv("GMAIL_APP_PASSWORD")

context = ssl.create_default_context()

try:
    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.starttls(context=context)
        smtp.login(EMAIL, PASSWORD)
        print("Login Successful!")
except Exception as e:
    print(e)