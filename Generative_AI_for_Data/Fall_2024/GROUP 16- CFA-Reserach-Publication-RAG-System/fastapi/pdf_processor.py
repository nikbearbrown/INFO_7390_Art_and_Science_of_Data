import fitz  # PyMuPDF
import io
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class PDFProcessor:
    def process_pdf(self, pdf_content: bytes) -> str:
        """
        Process PDF content and extract text.
        
        Args:
            pdf_content (bytes): The raw PDF content in bytes
            
        Returns:
            str: Extracted text from the PDF
        """
        try:
            # Open PDF from bytes
            doc = fitz.open(stream=pdf_content, filetype="pdf")
            
            # List to store text from each page
            text_content = []
            
            # Process each page
            for page_num in range(doc.page_count):
                try:
                    page = doc[page_num]
                    
                    # Extract text from the page
                    text = page.get_text()
                    
                    # Add page number for reference
                    page_text = f"Page {page_num + 1}:\n{text}\n"
                    text_content.append(page_text)
                    
                except Exception as e:
                    logger.error(f"Error processing page {page_num}: {str(e)}")
                    continue
            
            # Close the document
            doc.close()
            
            # Combine all text with proper spacing
            combined_text = "\n".join(text_content)
            
            # Basic text cleaning
            cleaned_text = self._clean_text(combined_text)
            
            return cleaned_text
            
        except Exception as e:
            logger.error(f"Error in PDF processing: {str(e)}")
            raise Exception(f"Failed to process PDF: {str(e)}")

    def _clean_text(self, text: str) -> str:
        """
        Clean extracted text by removing extra whitespace and normalizing line breaks.
        
        Args:
            text (str): Raw extracted text
            
        Returns:
            str: Cleaned text
        """
        try:
            # Replace multiple newlines with double newline
            cleaned = '\n'.join(line.strip() for line in text.splitlines() if line.strip())
            
            # Replace multiple spaces with single space
            cleaned = ' '.join(cleaned.split())
            
            # Add proper paragraph breaks
            cleaned = cleaned.replace('.', '.\n')
            
            return cleaned
            
        except Exception as e:
            logger.error(f"Error in text cleaning: {str(e)}")
            return text  # Return original text if cleaning fails

    def get_page_count(self, pdf_content: bytes) -> Optional[int]:
        """
        Get the total number of pages in the PDF.
        
        Args:
            pdf_content (bytes): The raw PDF content in bytes
            
        Returns:
            Optional[int]: Number of pages or None if counting fails
        """
        try:
            doc = fitz.open(stream=pdf_content, filetype="pdf")
            count = doc.page_count
            doc.close()
            return count
        except Exception as e:
            logger.error(f"Error getting page count: {str(e)}")
            return None

    def validate_pdf(self, pdf_content: bytes) -> bool:
        """
        Validate if the content is a valid PDF.
        
        Args:
            pdf_content (bytes): The raw PDF content in bytes
            
        Returns:
            bool: True if valid PDF, False otherwise
        """
        try:
            doc = fitz.open(stream=pdf_content, filetype="pdf")
            is_valid = doc.page_count > 0
            doc.close()
            return is_valid
        except Exception as e:
            logger.error(f"PDF validation failed: {str(e)}")
            return False