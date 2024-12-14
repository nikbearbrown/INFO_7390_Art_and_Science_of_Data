from fastapi import APIRouter, HTTPException, Response
from fast_api.services.pdfhandling import convert_markdown_to_pdf
import logging

router = APIRouter()

@router.get("/download-pdf/")
def convert_to_pdf(md_text: str):
    try:
        # Generate the file stream and metadata
        md_text = md_text

        pdf_content = convert_markdown_to_pdf(md_text)

        return Response(content=pdf_content, media_type="application/pdf")
    
    except Exception as e:
        logging.error("Exception:", e)
        raise HTTPException(status_code=500, detail=f"Error downloading the pdf: {str(e)}")
    