import datetime
import smtplib
import ssl
from datetime import timedelta
from email.message import EmailMessage

from fastapi import HTTPException, status
from jose import jwt, JWTError

SECRET_KEY = "1e0788a28e2e503315a3a894d353abaa36ace075faae8650f714d7c880f01da5"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def decode_permissions(permissions: int, permissions_list: list) -> dict:
    return {permission.name: bool(permissions & permission.value) for permission in permissions_list}


def create_token(payload: dict, duration: int = ACCESS_TOKEN_EXPIRE_MINUTES):
    payload["exp"] = datetime.datetime.now() + timedelta(minutes=duration)
    return jwt.encode(payload, SECRET_KEY, ALGORITHM)


def decode_token(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


"""Function for sending email to reset the password when the user forgert it"""

"""email_token_password : Not your gmail password, It's a password you generate from your gmail settings"""


def email_sender_for_pass_reset(email_sender, email_token_password, email_receiver):
    subject = "Reseting Password"

    # Read the HTML content from the template file
    with open('./resources/index.html', 'r') as html_file:
        body = html_file.read()

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['subject'] = subject
    em.set_content(body, subtype='html')

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login(email_sender, email_token_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())
