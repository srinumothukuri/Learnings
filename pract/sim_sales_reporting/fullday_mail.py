import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email import encoders
import glob
from datetime import date,timedelta
import subprocess

from datetime import datetime, timedelta

# Get today's date
today = datetime.now()

# Calculate yesterday's date
yesterday = today - timedelta(days=1)

# Format yesterday's date as YYYY-MM-DD
formatted_yesterday = yesterday.strftime('%Y-%m-%d')
hour = today.hour
hour=str(hour)
#hour = '0'

path='/home/ubuntu/summary'
#file_csv = glob.glob(path + "/*.csv")
file_csv = glob.glob(path + "/*"+formatted_yesterday+"_fullday.csv")
print(file_csv)
port = 587
#smtp_server = "smtp.gmail.com"
smtp_server = "smtp.office365.com"
#sender_email = "inficloudservice@gmail.com"
sender_email= "noreply_ug@lycamobile.ug"
demo = "W!24c@3s!d9e"
def send_mail(receiver_emal):
        receiver_em= receiver_emal
        print(receiver_em)
        mese = MIMEMultipart()
        #regx=glob.glob(path + "/*.csv")
        regx=glob.glob(path + "/*"+formatted_yesterday+"_fullday.csv")
        mail_content = '''
        Hi,
        Please find the attached files of sim sales live reporting.

        Thank you,
        Inficloud Team
        '''
        mese['From'] = sender_email
        mese['To']  = ', '.join(receiver_em)
        mese['Subject'] = "Sim sales realtime reporting"
        plain= MIMEText(mail_content, 'plain')
        for filenames in regx:
                attach_file = MIMEApplication(open(str(filenames),"r").read())
                name = filenames.split("/")[-1]
                attach_file.add_header('Content-Disposition', "attachment ; filename= %s"% name)
                mese.attach(attach_file)
        mese.attach(plain)
        session = smtplib.SMTP(smtp_server, port)
        session.ehlo()
        session.starttls()
        session.ehlo()
        session.login(sender_email, demo)
        session.sendmail(sender_email,receiver_em, mese.as_string())
        print(regx)
        session.quit()
        print("")
        print("Mail sent.")

#send_mail(['srinivas@inficloud.com','michael.mulindwa@lycamobile.ug'])
send_mail(['srinivas@inficloud.com'])
