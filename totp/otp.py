import os
import random
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

'''
OTP class is responsible for generating and saving the OTP code to a file.
It reads the OTP file path from the environment variables.
'''
class OTP:
    otp: str = ''

    def __init__(self):
        '''
        Initialize the OTP class with the OTP file path.
        '''
        try:
            self.file_path = os.getenv('OTP_FILE')
            # check to see if the file exists, if not create it
            if not os.path.exists(self.file_path):
                # create the file
                with open(self.file_path, 'w') as file:
                    self.otp = '00000'
                    file.write(self.otp)
                # generate a new OTP
                self.generate_otp()
                self.save_to_file()

#            self.otp = self.get_otp()
        except :
            pass
#            self.otp = ''


    def save_to_file(self):
        '''
        Save the OTP code to the file.
        :return: None
        '''
        if self.file_path:
            with open(self.file_path, 'w') as file:
                file.write(self.otp)
        else:
            raise ValueError("OTP_FILE path is not set in the environment variables")

    def get_otp(self):
        '''
        Get the OTP code from the file.
        If the OTP code is empty or None, generate a new OTP code.
        :return: OTP code
        '''
        if self.file_path:
            with open(self.file_path, 'r') as file:
                self.otp = file.read().strip()
            # if self.otp == '' or self.otp is None then generate a new OTP
            if self.otp == '' or self.otp is None:
                self.generate_otp()
            return self.otp
        else:
            raise ValueError("OTP_FILE path is not set in the environment variables")

    def generate_otp(self):
        '''
        Generate a new OTP code and save it to the file.
        :return: None
        '''
        current_otp = self.get_otp()
        new_otp = str(random.randint(23000, 88888))
        while new_otp == current_otp:
            new_otp = str(random.randint(23000, 88888))
        self.otp = new_otp
        self.save_to_file()
