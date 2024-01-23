from django.http import HttpResponse
from pdf2docx import Converter
import os



with open('resume.pdf', 'r') as f:
    pdf_file = f.read()

def convert_pdf_to_word_and_download():
    
    output_word_file_path = 'path/to/your/output/file.docx'

    if convert_pdf_to_word(pdf_file, output_word_file_path):
        try:
            # Open the converted Word file
            with open(output_word_file_path, 'rb') as file:
                response = HttpResponse(file.read(), content_type='application/msword')
                response['Content-Disposition'] = 'attachment; filename=output.docx'
                return response
        except Exception as e:
            return HttpResponse(str(e))
    else:
        return HttpResponse("Conversion failed")

def convert_pdf_to_word(pdf_file, output_word_path):
    try:
        # Create a Converter object
        if pdf_file:
            converter = Converter(pdf_file)
        else:
            raise Exception("PDF File not found")

        # Convert the PDF to Word
        converter.convert(output_word_path, start=0, end=None)

        # Close the Converter object
        converter.close()

        print(f"Conversion successful. Word file saved at: {output_word_path}")
        return True
    except Exception as e:
        print(f"Error converting PDF to Word: {e}")
        return False
    

convert_pdf_to_word_and_download()
