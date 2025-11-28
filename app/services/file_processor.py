from PyPDF2 import PdfReader
from docx import Document
from fastapi import UploadFile
import io

def extract_text_from_pdf(file_content: bytes) -> str:
    """Extract text from PDF file"""
    try:
        pdf_file = io.BytesIO(file_content)
        reader = PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        raise ValueError(f"Failed to extract text from PDF: {str(e)}")

def extract_text_from_docx(file_content: bytes) -> str:
    """Extract text from DOCX file"""
    try:
        docx_file = io.BytesIO(file_content)
        doc = Document(docx_file)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text.strip()
    except Exception as e:
        raise ValueError(f"Failed to extract text from DOCX: {str(e)}")

def extract_text_from_txt(file_content: bytes) -> str:
    """Extract text from TXT file"""
    try:
        return file_content.decode('utf-8').strip()
    except UnicodeDecodeError:
        # Try with different encoding
        try:
            return file_content.decode('latin-1').strip()
        except Exception as e:
            raise ValueError(f"Failed to extract text from TXT: {str(e)}")

async def process_file(file: UploadFile) -> str:
    """
    Process uploaded file and extract text based on file type.
    Supported types: PDF, DOCX, TXT
    """
    content = await file.read()
    filename = file.filename.lower()
    
    if filename.endswith('.pdf'):
        return extract_text_from_pdf(content)
    elif filename.endswith('.docx'):
        return extract_text_from_docx(content)
    elif filename.endswith('.txt'):
        return extract_text_from_txt(content)
    else:
        raise ValueError(f"Unsupported file type. Please upload PDF, DOCX, or TXT files.")
