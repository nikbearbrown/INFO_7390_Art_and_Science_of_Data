from fastapi import APIRouter, HTTPException, status
from fast_api.services.data_service import fetch_data_from_db, download_file
from fastapi.responses import StreamingResponse
import pandas as pd
from typing import List
import logging

router = APIRouter()

@router.get("/get-data/", response_model=List[dict])
def get_data():
    # Fetch data from the database
    data = fetch_data_from_db()
    if isinstance(data, pd.DataFrame):
        return data.to_dict(orient="records")
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No data returned from the database",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
@router.get("/extract-file/", response_class=StreamingResponse)
def extract_file(file_name: str):
    try:
        # Generate the file stream and metadata
        file_response = download_file(file_name)
        file_stream = file_response["pdf_content"]
        file_name = file_response["file_name"]
        file_path = file_response["file_path"]

        # Return a StreamingResponse for the binary data
        return StreamingResponse(
            file_stream,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={file_name}",
                     "X-File-Path": file_path}
        )
    except Exception as e:
        logging.error("Exception:", e)
        raise HTTPException(status_code=500, detail=f"Error extracting PDF for download: {str(e)}")



