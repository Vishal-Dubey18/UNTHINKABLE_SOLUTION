import os
import PyPDF2
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import logging

logger = logging.getLogger(__name__)

# Set Tesseract path for Windows
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class TextExtractor:
    def __init__(self):
        self.supported_formats = ['.pdf', '.png', '.jpg', '.jpeg']
    
    def extract_text(self, file_path):
        """Extract text from file based on its type"""
        try:
            file_ext = os.path.splitext(file_path)[1].lower()
            
            if file_ext == '.pdf':
                return self._extract_from_pdf(file_path)
            elif file_ext in ['.png', '.jpg', '.jpeg']:
                return self._extract_from_image(file_path)
            else:
                raise ValueError(f"Unsupported file format: {file_ext}")
                
        except Exception as e:
            logger.error(f"Error extracting text from {file_path}: {str(e)}")
            raise
    
    def _extract_from_pdf(self, file_path):
        """Extract text from PDF file"""
        try:
            # First try direct text extraction
            text = self._extract_pdf_text(file_path)
            
            # If no text found, try OCR
            if not text or len(text.strip()) < 50:
                text = self._extract_pdf_ocr(file_path)
                
            return text
            
        except Exception as e:
            logger.error(f"PDF extraction failed: {str(e)}")
            raise
    
    def _extract_pdf_text(self, file_path):
        """Extract text directly from PDF"""
        text = ""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    page_text = page.extract_text()
                    if page_text:
                        text += f"--- Page {page_num + 1} ---\n{page_text}\n\n"
                        
        except Exception as e:
            logger.warning(f"Direct PDF text extraction failed: {str(e)}")
            
        return text
    
    def _extract_pdf_ocr(self, file_path):
        """Extract text from PDF using OCR"""
        text = ""
        try:
            # Convert PDF to images
            images = convert_from_path(file_path, dpi=200)
            
            for i, image in enumerate(images):
                # Convert PIL image to RGB if needed
                if image.mode != 'RGB':
                    image = image.convert('RGB')
                
                # Perform OCR
                page_text = pytesseract.image_to_string(image)
                text += f"--- Page {i + 1} ---\n{page_text}\n\n"
                
        except Exception as e:
            logger.error(f"PDF OCR failed: {str(e)}")
            raise
            
        return text
    
    def _extract_from_image(self, file_path):
        """Extract text from image using OCR"""
        try:
            # Open and preprocess image
            image = Image.open(file_path)
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Configure Tesseract for better accuracy
            custom_config = r'--oem 3 --psm 6'
            
            # Perform OCR
            text = pytesseract.image_to_string(image, config=custom_config)
            
            return text if text.strip() else "No text could be extracted from this image."
            
        except Exception as e:
            logger.error(f"Image OCR failed: {str(e)}")
            return f"OCR processing error: {str(e)}"