# src/app/utils/pdf.py
# Small helpers for PDF handling (wrapper around pdfplumber)
import pdfplumber
import io

def extract_tables_from_pdf_bytes(binary: bytes):
    with pdfplumber.open(io.BytesIO(binary)) as pdf:
        pages_tables = []
        for p in pdf.pages:
            pages_tables.append(p.extract_tables())
        return pages_tables
