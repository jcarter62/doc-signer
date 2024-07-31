import os
from PyPDF2 import PdfReader, PdfWriter
import tempfile

class PDFCopier:
    def __init__(self, input_filename, output_filename, quantity):
        self.input_filename = input_filename
        self.quantity = int(quantity)

        # if output_filename is not provided, create a temporary file
        if output_filename:
            self.output_filename = output_filename
        else:
            with tempfile.NamedTemporaryFile() as temp_file:
                self.output_filename = temp_file.name + '.pdf'

    def copy_pdfs(self):
        if not os.path.exists(self.input_filename):
            raise FileNotFoundError(f"Input file {self.input_filename} does not exist")

        reader = PdfReader(self.input_filename)
        writer = PdfWriter()

        for x in range(self.quantity):
            for page_num in range(len(reader.pages)):
                writer.add_page(reader.pages[page_num])

        with open(self.output_filename, 'wb') as output_file:
            writer.write(output_file)

# Example usage:
# copier = PDFCopier('input.pdf', 'output.pdf', 5)
# copier.copy_pdfs()