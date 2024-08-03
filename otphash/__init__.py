import hashlib


'''
This module provides a class to hash OTP values using a specified algorithm.
'''
class OTPHasher:
    def __init__(self, algorithm='sha256'):
        self.algorithm = algorithm

    def hash_otp(self, otp_value):
        '''
        Hash the OTP value using the specified algorithm.
        :param otp_value:
        :return: hashed OTP value
        '''
        if not otp_value:
            raise ValueError("OTP value cannot be empty")

        hash_function = hashlib.new(self.algorithm)
        hash_function.update(otp_value.encode('utf-8'))
        return hash_function.hexdigest()


