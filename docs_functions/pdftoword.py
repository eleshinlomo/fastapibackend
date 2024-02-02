from pdf2docx import Converter
from io import BytesIO
from fastapi import FastAPI, File, UploadFile, HTTPException


def convert_pdf_to_docx(pdf):
    try:
        cv = Converter(pdf)
        docx_stream = BytesIO()
        cv.convert(docx_stream, start=0, end=None)
        docx_stream.seek(0)
        return docx_stream.read()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
