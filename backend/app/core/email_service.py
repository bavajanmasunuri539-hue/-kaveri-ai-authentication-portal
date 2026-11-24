import base64
import json
from email.mime.text import MIMEText
from pathlib import Path

from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

load_dotenv()

TOKEN_FILE = Path(__file__).resolve().parents[2] / "gmail_token.json"

SCOPES = [
    "https://www.googleapis.com/auth/gmail.send"
]


def send_password_reset_email(recipient: str, reset_url: str):
    if not TOKEN_FILE.exists():
        raise RuntimeError("Gmail authorization is required")

    token_data = json.loads(TOKEN_FILE.read_text(encoding="utf-8"))

    credentials = Credentials(
        token=None,
        refresh_token=token_data["refresh_token"],
        token_uri=token_data["token_uri"],
        client_id=__import__("os").getenv("GOOGLE_CLIENT_ID"),
        client_secret=__import__("os").getenv("GOOGLE_CLIENT_SECRET"),
        scopes=SCOPES
    )

    credentials.refresh(Request())

    message = MIMEText(
        f"""Hello,

We received a request to reset your KAVERI AI password.

Click the link below to reset your password:

{reset_url}

This link expires in 15 minutes.

If you did not request this, please ignore this email.

Regards,
KAVERI AI Team
"""
    )

    message["to"] = recipient
    message["from"] = token_data["email"]
    message["subject"] = "KAVERI AI - Password Reset"

    raw_message = base64.urlsafe_b64encode(
        message.as_bytes()
    ).decode("utf-8")

    service = build(
        "gmail",
        "v1",
        credentials=credentials,
        cache_discovery=False
    )

    service.users().messages().send(
        userId="me",
        body={"raw": raw_message}
    ).execute()

    return True
