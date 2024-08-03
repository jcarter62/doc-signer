import os
import subprocess
from dotenv import load_dotenv
from .pdfcopier import PDFCopier

# Load environment variables from .env file
load_dotenv()

'''
PDFPrinter class is responsible for printing a PDF file to a printer.
It reads the printer executable, printer name and PDF file from the environment variables.
It uses the subprocess library to run the printer executable with the specified arguments.
'''
class PDFPrinter:
    _cmdline = ''
    _copier = None
    _output_file = None

    def __init__(self, qty=1):
        '''
        Initialize the PDFPrinter class with the printer executable, printer name and PDF file.
        '''
        self.printer_exe = os.getenv('PRINTER_EXE')
        self.printer = os.getenv('PRINTER1')
        self.pdf_file = os.getenv('PDFFILE')
        self.qty = qty
        self._cmdline = ''
        # generate a pdf with QTY copies of the pdf_file

    def _create_command(self):
        '''
        Create the command line to print the PDF file using the printer executable and printer name.
        :return:
        '''
        if not all([self.printer_exe, self.printer, self._output_file]):
            raise ValueError("One or more environment variables are not set")
        # self._cmdline = f'"{self.printer_exe}" "{self.pdf_file}" "{self.printer}" copies={self.qty} /s'
        self._cmdline = f'"{self.printer_exe}" "{self._output_file}" "{self.printer}" /s'

    def print(self):
        '''
        Print the PDF file using the printer executable and printer name.
        :return:
        '''
        self._create_command()
        try:
            subprocess.run(self._cmdline, check=True, shell=True)
        except Exception as e:
            print(f"An error occurred: {e}")

    def print_async(self):
        '''
        Print the PDF file asynchronously using the printer executable and printer name.
        :return:
        '''
        try:
            # Remove old output files
            self.cleanup_output_files()
            # Create a new output file
            self._copier = PDFCopier(self.pdf_file, None, self.qty)
            self._output_file = self._copier.output_filename
            self._copier.copy_pdfs()
            self.save_output_file_name(self._output_file)
            #
            self._create_command()
            #
            subprocess.Popen(self._cmdline, shell=True)
        except Exception as e:
            print(f"An error occurred: {e}")


    def save_output_file_name(self, output_file: str):
        '''
        Save the output file name to a list for cleanup later.
        :param output_file:
        :return: None
        '''
        output_file_list = os.getenv('OUTPUT_FILE_LIST')
        if not output_file_list:
            raise ValueError("OUTPUT_FILE_LIST environment variable is not set")

        with open(output_file_list, 'a') as file:
            file.write(output_file + '\n')

    def cleanup_output_files(self):
        '''
        Remove the output files that were created during printing.
        :return: None
        '''
        output_file_list = os.getenv('OUTPUT_FILE_LIST')
        if not output_file_list:
            raise ValueError("OUTPUT_FILE_LIST environment variable is not set")

        # check to see if the file exists
        if not os.path.exists(output_file_list):
            return
        # Read the current list of output files
        with open(output_file_list, 'r') as file:
            lines = file.readlines()

        # Remove each file and collect filenames to be removed from the list
        remaining_files = []
        for line in lines:
            file_path = line.strip()
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except Exception as e:
                    print(f"Error removing file {file_path}: {e}")
                    remaining_files.append(file_path)
            else:
                remaining_files.append(file_path)

        # Rewrite the output file list excluding the removed files
        with open(output_file_list, 'w') as file:
            for file_path in remaining_files:
                file.write(file_path + '\n')

