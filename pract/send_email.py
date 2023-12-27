

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime

def send_email():
    current_date = datetime.date.today().strftime('%Y-%m-%d')
    port = 587
    smtp_server = "email-smtp.us-east-2.amazonaws.com"
    sender = "AKIAZ4L77MD6R4WER5HW"
    sender_email = "noreply@infimobile.com"
    receiver_email = ['m.srinivas2373@gmail.com']
    demo = "BNiXaZbYRlWDGdiw9y7+AqxLmdSXN8n/dcjJHKkJZArS"
    msg = MIMEMultipart()
    msg['To'] = ', '.join(receiver_email)
    message = f"No processed CDRs found on {current_date}."
    msg['SUBJECT'] = 'VIP Processed cdrs report'
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
