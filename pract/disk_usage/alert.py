


import smtplib
import socket
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import sys  # Import the sys module

# Get the server's IP address
server_ip = socket.gethostbyname(socket.gethostname())

# Check if the correct number of command-line arguments is provided
#if len(sys.argv) != 3:
#    print("Usage: python your_email_script.py <message> <subject>")
#    sys.exit(1)

# Command-line arguments for email content and subject
mail_content = sys.argv[1]
subject = sys.argv[2]

# Rest of your code remains the same
port = 587
smtp_server = "smtp.office365.com"
sender_email = "noreply_ug@lycamobile.ug"
receiver_email = ['srinivas@inficloud.com']
demo = "W!24c@3s!d9e"
message = MIMEMultipart()
message['From'] = sender_email
message['To'] = ', '.join(receiver_email)
message['Subject'] = subject  # Use the subject provided as a command-line argument

# Include the server's IP address in the email content
# Include the server's IP address in the email content
#mail_content += "\n\nServer IP: " + server_ip


def report_mail():
    html  = MIMEText(mail_content, 'html')
    message.attach(html)

    session = smtplib.SMTP(smtp_server, port)
    session.ehlo()
    session.starttls()
    session.ehlo()
    session.login(sender_email, demo)
    session.sendmail(sender_email, receiver_email, message.as_string())
    session.quit()

report_mail()

