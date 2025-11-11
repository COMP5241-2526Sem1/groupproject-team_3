"""
Document Processing Service
Extracts text content from PDF and PowerPoint files
"""

import logging
from typing import Optional
import io

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_text_from_pdf(file_content: bytes) -> str:
    """
    Extract text from PDF file
    
    Args:
        file_content (bytes): PDF file content
        
    Returns:
        str: Extracted text content
    """
    try:
        from PyPDF2 import PdfReader
        
        pdf_file = io.BytesIO(file_content)
        reader = PdfReader(pdf_file)
        
        text_content = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                text_content.append(text)
        
        extracted_text = '\n\n'.join(text_content)
        logger.info(f"Extracted {len(extracted_text)} characters from PDF")
        
        return extracted_text
        
    except Exception as e:
        logger.error(f"PDF extraction error: {e}")
        raise Exception(f"Failed to extract PDF content: {str(e)}")


def extract_text_from_pptx(file_content: bytes) -> str:
    """
    Extract text from PowerPoint file
    
    Args:
        file_content (bytes): PowerPoint file content
        
    Returns:
        str: Extracted text content
    """
    try:
        from pptx import Presentation
        
        pptx_file = io.BytesIO(file_content)
        prs = Presentation(pptx_file)
        
        text_content = []
        
        for slide_num, slide in enumerate(prs.slides, 1):
            slide_text = [f"--- Slide {slide_num} ---"]
            
            # Extract text from shapes
            for shape in slide.shapes:
                if hasattr(shape, "text") and shape.text:
                    slide_text.append(shape.text)
            
            # Extract text from tables
            if hasattr(slide, 'shapes'):
                for shape in slide.shapes:
                    if shape.has_table:
                        for row in shape.table.rows:
                            row_text = []
                            for cell in row.cells:
                                if cell.text:
                                    row_text.append(cell.text)
                            if row_text:
                                slide_text.append(' | '.join(row_text))
            
            if len(slide_text) > 1:  # Has content beyond the header
                text_content.append('\n'.join(slide_text))
        
        extracted_text = '\n\n'.join(text_content)
        logger.info(f"Extracted {len(extracted_text)} characters from PPTX ({len(prs.slides)} slides)")
        
        return extracted_text
        
    except Exception as e:
        logger.error(f"PPTX extraction error: {e}")
        raise Exception(f"Failed to extract PowerPoint content: {str(e)}")


def extract_document_content(filename: str, file_content: bytes) -> str:
    """
    Extract text content from document based on file extension
    
    Args:
        filename (str): Name of the file
        file_content (bytes): File content
        
    Returns:
        str: Extracted text content
    """
    filename_lower = filename.lower()
    
    if filename_lower.endswith('.pdf'):
        return extract_text_from_pdf(file_content)
    elif filename_lower.endswith(('.ppt', '.pptx')):
        return extract_text_from_pptx(file_content)
    else:
        raise ValueError(f"Unsupported file format: {filename}. Only PDF and PowerPoint files are supported.")


def summarize_content(text: str, max_length: int = 3000) -> str:
    """
    Summarize or truncate content to fit within AI token limits
    
    Args:
        text (str): Full text content
        max_length (int): Maximum character length
        
    Returns:
        str: Summarized or truncated text
    """
    if len(text) <= max_length:
        return text
    
    # Truncate to max_length and add ellipsis
    truncated = text[:max_length]
    
    # Try to cut at a sentence or paragraph boundary
    for delimiter in ['\n\n', '\n', '. ', ' ']:
        last_index = truncated.rfind(delimiter)
        if last_index > max_length * 0.9:  # Within 10% of max length
            return truncated[:last_index] + delimiter + "... (content truncated)"
    
    return truncated + "... (content truncated)"
