import os
import subprocess
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class PDFPrinter:
    _cmdline = ''

    def __init__(self, qty=1):
        self.printer_exe = os.getenv('PRINTER_EXE')
        self.printer = os.getenv('PRINTER1')
        self.pdf_file = os.getenv('PDFFILE')
        self.qty = qty
        self._cmdline = ''

    def _create_command(self):
        if not all([self.printer_exe, self.printer, self.pdf_file]):
            raise ValueError("One or more environment variables are not set")
        self._cmdline = f'"{self.printer_exe}" "{self.pdf_file}" "{self.printer}" copies={self.qty} /s'

    def print(self):
        self._create_command()
        try:
            subprocess.run(self._cmdline, check=True, shell=True)
        except Exception as e:
            print(f"An error occurred: {e}")


    def print_async(self):
        self._create_command()
        try:
            subprocess.Popen(self._cmdline, shell=True)
        except Exception as e:
            print(f"An error occurred: {e}")
