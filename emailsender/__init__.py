import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
from totp import OTP

# Load environment variables from .env file
load_dotenv()

'''
EmailSender class is responsible for sending OTP code to the user's email.
It reads the email server, port, recipient email and sender email from the environment variables.
It uses the smtplib library to send the email.
'''
class EmailSender:
    def __init__(self):
        '''
        Initialize the EmailSender class with the email server, port, recipient email and sender email.
        '''
        self.recipient_email = os.getenv('EMAIL')
        self.email_server = os.getenv('EMAIL_SERVER')
        self.email_port = int(os.getenv('EMAIL_PORT'))
        self.email_from = os.getenv('EMAIL_FROM')

    def send_email(self):
        '''
        Send the OTP code to the recipient email.
        :return:
        '''
        if not all([self.recipient_email, self.email_server, self.email_port, self.email_from]):
            raise ValueError("One or more environment variables are not set")

        otp = OTP()
        otp_value = otp.get_otp()

        msg = MIMEText(f"Your OTP is: {otp_value}")
        msg['Subject'] = 'Your OTP Code'
        msg['From'] = self.email_from
        msg['To'] = self.recipient_email

        with smtplib.SMTP(self.email_server, self.email_port) as server:
            server.sendmail(self.email_from, self.recipient_email, msg.as_string())

