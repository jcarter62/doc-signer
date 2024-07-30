from flask import Flask, render_template, redirect, request, send_from_directory
import jinja2
from totp import OTP
from pdfprinter import PDFPrinter
from emailsender import EmailSender
from otphash import OTPHasher
import logging
import os


app = Flask(__name__)


@app.route('/')
def home_route():  # put application's code here
    logging.info('Home route accessed')
    otp = OTP()
    otpvalue = otp.get_otp()
    hotp = OTPHasher().hash_otp(otpvalue)
    return render_template('home.html', otp=hotp, message='')

@app.route('/favicon.ico')
def favicon():
    logging.info('Favicon route accessed')
    return send_from_directory( os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/new-otp')
def new_otp():
    logging.info('New OTP route accessed')
    otp = OTP()
    otp.generate_otp()
    otpvalue = otp.get_otp()
    hotp = OTPHasher().hash_otp(otpvalue)

    es = EmailSender()
    es.send_email()
    return render_template('home.html', otp=hotp, message='Check your email for a new OTP Code')


@app.route('/verify-otp', methods=['POST'])
def verify_otp():
    logging.info('Verify OTP route accessed')
    # get the otp from the form
    entered_otp = request.form['otp']
    entered_hotp = OTPHasher().hash_otp(entered_otp)
    otp = OTP()
    otpvalue = otp.get_otp()
    hotp = OTPHasher().hash_otp(otpvalue)


    if entered_hotp == hotp:
        return render_template('success.html', otp=hotp, message='')
    else:
        return redirect('/')

@app.route('/print-signature', methods=['POST'])
def print_signature():
    logging.info('Print signature route accessed')
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
