import io
import os
import sys
from typing import Union, BinaryIO
from pypdf import PdfReader
import docx

def extract_text_from_pdf(file_input: Union[str, bytes, BinaryIO]) -> str:
    """
    Extracts plain text from a PDF file path, bytes, or file-like object using pypdf.
    Raises clear errors for empty, unreadable, or corrupted files.
    """
    try:
        if isinstance(file_input, str):
            if not os.path.exists(file_input):
                raise FileNotFoundError(f"File not found: '{file_input}'")
            with open(file_input, "rb") as f:
                stream = io.BytesIO(f.read())
        elif isinstance(file_input, bytes):
            stream = io.BytesIO(file_input)
        else:
            # File-like object (e.g. Streamlit UploadedFile)
            if hasattr(file_input, "getvalue"):
                stream = io.BytesIO(file_input.getvalue())
            elif hasattr(file_input, "read"):
                stream = io.BytesIO(file_input.read())
                if hasattr(file_input, "seek"):
                    file_input.seek(0)
            else:
                stream = file_input
            
        reader = PdfReader(stream)
        if len(reader.pages) == 0:
            raise ValueError("The PDF document contains 0 pages or is empty.")
            
        extracted_pages = []
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text and text.strip():
                extracted_pages.append(text.strip())
                
        full_text = "\n\n".join(extracted_pages)
        if not full_text.strip():
            raise ValueError("The PDF document does not contain readable text (it may be scanned/image-only or blank).")
        return full_text
    except ValueError as ve:
        raise ve
    except Exception as e:
        raise RuntimeError(f"Corrupted or invalid PDF file: {str(e)}")

def extract_text_from_docx(file_input: Union[str, bytes, BinaryIO]) -> str:
    """
    Extracts plain text from a DOCX file path, bytes, or file-like object using python-docx.
    Raises clear errors for empty or corrupted files.
    """
    try:
        if isinstance(file_input, str):
            if not os.path.exists(file_input):
                raise FileNotFoundError(f"File not found: '{file_input}'")
            with open(file_input, "rb") as f:
                stream = io.BytesIO(f.read())
        elif isinstance(file_input, bytes):
            stream = io.BytesIO(file_input)
        else:
            if hasattr(file_input, "getvalue"):
                stream = io.BytesIO(file_input.getvalue())
            elif hasattr(file_input, "read"):
                stream = io.BytesIO(file_input.read())
                if hasattr(file_input, "seek"):
                    file_input.seek(0)
            else:
                stream = file_input
                
        doc = docx.Document(stream)
        paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
        
        for table in doc.tables:
            for row in table.rows:
                row_text = " | ".join(cell.text.strip() for cell in row.cells if cell.text.strip())
                if row_text:
                    paragraphs.append(row_text)
                    
        full_text = "\n\n".join(paragraphs)
        if not full_text.strip():
            raise ValueError("The DOCX document is empty.")
        return full_text
    except ValueError as ve:
        raise ve
    except Exception as e:
        raise RuntimeError(f"Corrupted or invalid DOCX file: {str(e)}")

def get_text(uploaded_file: Union[str, bytes, BinaryIO], filename: str = None) -> str:
    """
    Primary extraction interface. Extracts text from PDF files (using pypdf)
    and DOCX files (using python-docx). Raises clear errors for unsupported
    file types or corrupted files.
    """
    if uploaded_file is None:
        raise ValueError("No file was provided for text extraction.")
        
    name = filename or getattr(uploaded_file, "name", "")
    if not name and isinstance(uploaded_file, str):
        name = uploaded_file
        
    lower_name = name.lower()
    if lower_name.endswith(".pdf"):
        return extract_text_from_pdf(uploaded_file)
    elif lower_name.endswith(".docx"):
        return extract_text_from_docx(uploaded_file)
    else:
        ext = os.path.splitext(name)[1] if name else "unknown"
        raise ValueError(f"Unsupported file format '{ext}'. Only PDF (.pdf) and DOCX (.docx) files are supported.")

# Alias for backward compatibility across modules
extract_text = get_text

if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

    if len(sys.argv) > 1:
        target_path = sys.argv[1]
        try:
            print(f"Extracting text from: {target_path}")
            result_text = get_text(target_path)
            print("=" * 60)
            print(result_text)
            print("=" * 60)
            print(f"Extraction successful! Total characters: {len(result_text)}")
        except Exception as err:
            print(f"Extraction Error: {err}", file=sys.stderr)
            sys.exit(1)
    else:
        print("Usage: python logic/extract_text.py <path_to_pdf_or_docx>")
