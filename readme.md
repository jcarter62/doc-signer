# OTP Verification and Signature Printing Application

This application provides OTP (One-Time Password) generation and verification, along with a feature to print signatures on checks. It is built using Flask and includes logging for important events.

## Prerequisites

- Python 3.6+
- pip (Python package installer)
- Virtual environment (optional but recommended)

## Installation

1. **Clone the repository:**

    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Create and activate a virtual environment (optional but recommended):**

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages:**

    ```sh
    pip install -r requirements.txt
    ```

4. **Set up environment variables:**

    Create a `.env` file in the root directory of the project and add the following variables:

    ```env
    HOST=0.0.0.0
    PORT=5000
    ```

## Configuration

1. **Static Files:**

    Ensure that the image files are placed in the `static` directory. For example, `pen-writing-on-check.png` should be located at `static/pen-writing-on-check.png`.

2. **Templates:**

    The HTML templates are located in the `templates` directory. You can customize `home.html` and `success.html` as needed.

## Running the Application

1. **Start the application using `run.py`:**

    ```sh
    python run.py
    ```

    This will start the server with logging configured in `run.py`.

## Logging

Logging is configured in `run.py` to log important events and errors to the console. You can view the logs in the terminal where you start the application.

## Usage

1. **Generate OTP:**

    Navigate to the home page and click on "Generate New OTP Code". The OTP will be sent to your email.

2. **Verify OTP:**

    Enter the OTP code received in your email and click "Verify OTP Code".

3. **Print Signature:**

    After OTP verification, enter the quantity of signatures to print and click "Print".

## External Resources

- [PDF to Printer](https://mendelson.org/pdftoprinter.html)
- Artwork:
  - [Wannapik Vector 1](https://www.wannapik.com/vectors/65020)
  - [Wannapik Vector 2](https://www.wannapik.com/vectors/62668?search%5Bquery%5D=printing)