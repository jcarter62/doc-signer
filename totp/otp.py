import os
import random
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class OTP:
    otp: str = ''

    def __init__(self):
        try:
            self.file_path = os.getenv('OTP_FILE')
            # check to see if the file exists, if not create it
            if not os.path.exists(self.file_path):
                self.save_to_file()

            self.otp = self.get_otp()
        except :
            self.otp = ''


    def save_to_file(self):
        if self.file_path:
            with open(self.file_path, 'w') as file:
                file.write(self.otp)
        else:
            raise ValueError("OTP_FILE path is not set in the environment variables")

    def get_otp(self):
        if self.file_path:
            with open(self.file_path, 'r') as file:
                self.otp = file.read().strip()
            return self.otp
        else:
            raise ValueError("OTP_FILE path is not set in the environment variables")

    def generate_otp(self):
        current_otp = self.get_otp()
        new_otp = str(random.randint(23000, 88888))
        while new_otp == current_otp:
            new_otp = str(random.randint(23000, 88888))
        self.otp = new_otp
        self.save_to_file()
