from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel
import subprocess
import tempfile
import os
from fast_api.services.google_codelabs import create_codelab_from_string, serve_codelab
router = APIRouter()

class CodelabContent(BaseModel):
    content: str

@router.get("/create-codelab")
def create_codelab(content: CodelabContent):
    md_text = content.content
    create_codelab_from_string(md_text)