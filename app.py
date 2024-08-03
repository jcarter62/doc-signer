from flask import Flask, render_template, redirect, request, send_from_directory
import jinja2
from totp import OTP
from pdfprinter import PDFPrinter
from emailsender import EmailSender
from otphash import OTPHasher
import logging
import os

sep = ' | '

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(message)s')

app = Flask(__name__)


def format_log_entry():
    '''
    Format the log entry with the remote IP, date, method, path, scheme, status code, content length and user agent.
    :return: log entry text
    '''
    # def format_log_entry():
    #     user_agent = request.headers.get('User-Agent')
    #     return f'{request.remote_addr} - - [{request.date}] "{request.method} {request.path} {request.scheme}/{request.environ.get("SERVER_PROTOCOL")}" {request.status_code} {request.content_length} "{user_agent}"'
    user_agent = request.headers.get('User-Agent')

    if 'HTTP_CF_CONNECTING_IP' not in request.headers.environ:
        remote_ip = request.remote_addr
    else:
        remote_ip = request.headers.environ['HTTP_CF_CONNECTING_IP']

    msg = f'{remote_ip}{sep}[{request.date}] {request.method} '
    msg = msg + f'{request.scheme}:{request.path} {sep}'
    msg = msg + user_agent
    return msg


@app.before_request
def log_request_info():
    '''
    Log the request information before processing the request.
    :return:
    '''
    logging.info(format_log_entry())


@app.route('/')
def home_route():  # put application's code here
    '''
    Home route to display home page with a few buttons.
    :return:
    '''
    otp = OTP()
    otpvalue = otp.get_otp()
    hotp = OTPHasher().hash_otp(otpvalue)
    return render_template('home.html', otp=hotp, message='')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory( os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/new-otp')
def new_otp():
    '''
    Generate a new OTP and send it to the user's email.
    Display home page with a message suggesting the user to check their email,
    also send the hashed OTP to the home page for use to verify the entered OTP.
    :return:
    '''
    otp = OTP()
    otp.generate_otp()
    otpvalue = otp.get_otp()
    hotp = OTPHasher().hash_otp(otpvalue)

    es = EmailSender()
    es.send_email()
    return render_template('home.html', otp=hotp, message='Check your email for a new OTP Code')


@app.route('/verify-otp', methods=['POST'])
def verify_otp():
    '''
    Verify the OTP entered by the user.
    If the OTP is correct, display the success page.
    :return:
    '''
    # get the otp from the form
    entered_otp = request.form['otp']
    entered_hotp = OTPHasher().hash_otp(entered_otp)
    otp = OTP()
    otpvalue = otp.get_otp()
    hotp = OTPHasher().hash_otp(otpvalue)

    if entered_hotp == hotp:
        # remove old output files
        return render_template('success.html', otp=hotp, message='')
    else:
        return redirect('/')

@app.route('/print-signature', methods=['POST'])
def print_signature():
    '''
    Print the signature based on the quantity entered by the user
    if the OTP matches the current OTP saved in the file.
    '''
    # get the otp from the form, which is already hashed.
    entered_hotp = request.form['otp']

    # check against the current otp stored.
    otp = OTP()
    hotp = OTPHasher().hash_otp(otp.get_otp())
    if entered_hotp == hotp:
        # retrieve the quantity from the form
        quantity = request.form['quantity']
        msg = ''
        if quantity > '':
            if int(quantity) > 0:
                pdf = PDFPrinter(qty=quantity)
                # pdf.print()
                pdf.print_async()
                msg = f'Printing signature x {quantity} ... confirm with staff.'
            else:
                msg = 'Please enter a quantity >= 1'
        else:
            msg = 'Please enter a valid quantity'
        return render_template('success.html', otp=entered_hotp, message=msg)
    else:
        return redirect('/')


if __name__ == '__main__':
    app.run( )
