

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime
import sys

def send_email():
    certificate_name = sys.argv[1]
    expiry_date = sys.argv[2]
    current_date = datetime.date.today().strftime('%Y-%m-%d')
    port = 587
    smtp_server = "email-smtp.us-east-2.amazonaws.com"
    sender = "AKIAZ4L77MD6R4WER5HW"
    sender_email = "noreply@infimobile.com"
    receiver_email = ['m.srinivas2374@gmail.com']
    demo = "BNiXaZbYRlWDGdiw9y7+AqxLmdSXN8n/dcjJHKkJZArS"
    msg = MIMEMultipart()
    msg['To'] = ', '.join(receiver_email)
    message = f"{certificate_name} is going to expire on {expiry_date} IST."
    msg['SUBJECT'] = 'Certificate expiry alert '
    part1 = MIMEText(message, 'plain')
    msg.attach(part1)
    server = smtplib.SMTP(smtp_server, port)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(sender, demo)
    server.sendmail(sender_email, receiver_email, msg.as_string())
    server.quit()

send_email()
