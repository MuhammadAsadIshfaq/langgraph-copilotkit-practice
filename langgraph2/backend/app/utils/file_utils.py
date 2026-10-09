import io
import PyPDF2
import docx
import mammoth
from typing import Union

def extract_text_from_pdf(file_content: bytes) -> str:
    """Extract text from PDF file content."""
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text

def extract_text_from_docx(file_content: bytes) -> str:
    """Extract text from DOCX file content."""
    doc = docx.Document(io.BytesIO(file_content))
    text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
    return text

def extract_text_from_doc(file_content: bytes) -> str:
    """Extract text from DOC file content using mammoth."""
    result = mammoth.convert_to_html(io.BytesIO(file_content))
    text = result.value
    return text

def extract_resume_text(file_content: bytes, file_type: str) -> str:
    """Extract text from resume file based on file type."""
    if file_type.lower().endswith('.pdf'):
        return extract_text_from_pdf(file_content)
    elif file_type.lower().endswith('.docx'):
        return extract_text_from_docx(file_content)
    elif file_type.lower().endswith('.doc'):
        return extract_text_from_doc(file_content)
    else:
        raise ValueError("Unsupported file format. Please upload PDF, DOC, or DOCX files.") 