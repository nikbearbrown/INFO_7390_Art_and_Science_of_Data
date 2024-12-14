# SPDX-FileCopyrightText: Copyright (c) 2023-2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

import os
import base64
import logging
from typing import List, Optional
from io import BytesIO
from fastapi import UploadFile, HTTPException
from PIL import Image
import requests
import PyPDF2
from llama_index.core import Document
from llama_index.llms.nvidia import NVIDIA

# Set up logging
logger = logging.getLogger(__name__)

def set_environment_variables():
    """Set necessary environment variables."""
    os.environ["NVIDIA_API_KEY"] = "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"

def get_b64_image_from_content(image_content: bytes) -> str:
    """Convert image content to base64 encoded string."""
    img = Image.open(BytesIO(image_content))
    if img.mode != 'RGB':
        img = img.convert('RGB')
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

def is_graph(image_content: bytes) -> bool:
    """Determine if an image is a graph, plot, chart, or table."""
    res = describe_image(image_content)
    return any(keyword in res.lower() for keyword in ["graph", "plot", "chart", "table"])

def process_graph(image_content: bytes) -> str:
    """Process a graph image and generate a description."""
    deplot_description = process_graph_deplot(image_content)
    mixtral = NVIDIA(model="meta/llama-3.1-70b-instruct")
    response = mixtral.complete(
        "Your responsibility is to explain charts. You are an expert in describing "
        "the responses of linearized tables into plain English text for LLMs to use. "
        "Explain the following linearized table. " + deplot_description
    )
    return response.text

def describe_image(image_content: bytes) -> str:
    """Generate a description of an image using NVIDIA API."""
    image_b64 = get_b64_image_from_content(image_content)
    invoke_url = "https://ai.api.nvidia.com/v1/vlm/nvidia/neva-22b"
    api_key = os.getenv("NVIDIA_API_KEY")
    
    if not api_key:
        raise ValueError("NVIDIA API Key is not set. Please set the NVIDIA_API_KEY environment variable.")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json"
    }

    payload = {
        "messages": [
            {
                "role": "user",
                "content": f'Describe what you see in this image. <img src="data:image/png;base64,{image_b64}" />'
            }
        ],
        "max_tokens": 1024,
        "temperature": 0.20,
        "top_p": 0.70,
        "seed": 0,
        "stream": False
    }

    response = requests.post(invoke_url, headers=headers, json=payload)
    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail="Failed to process image with NVIDIA API"
        )
    return response.json()["choices"][0]['message']['content']

def process_graph_deplot(image_content: bytes) -> str:
    """Process a graph image using NVIDIA's Deplot API."""
    invoke_url = "https://ai.api.nvidia.com/v1/vlm/google/deplot"
    image_b64 = get_b64_image_from_content(image_content)
    api_key = os.getenv("NVIDIA_API_KEY")
    
    if not api_key:
        raise ValueError("NVIDIA API Key is not set. Please set the NVIDIA_API_KEY environment variable.")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json"
    }

    payload = {
        "messages": [
            {
                "role": "user",
                "content": f'Generate underlying data table of the figure below: <img src="data:image/png;base64,{image_b64}" />'
            }
        ],
        "max_tokens": 1024,
        "temperature": 0.20,
        "top_p": 0.20,
        "stream": False
    }

    response = requests.post(invoke_url, headers=headers, json=payload)
    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail="Failed to process graph with Deplot API"
        )
    return response.json()["choices"][0]['message']['content']

async def process_text_document(content: bytes, extension: str) -> str:
    """Extract text from various document types, with special handling for PDFs."""
    if extension == '.pdf':
        try:
            pdf_file = BytesIO(content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text_content = []
            for page in pdf_reader.pages:
                text = page.extract_text()
                if text.strip():
                    text_content.append(text.strip())
            return "\n\n".join(text_content)
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to process PDF file: {str(e)}"
            )
    else:
        try:
            return content.decode('utf-8')
        except UnicodeDecodeError:
            try:
                return content.decode('latin-1')
            except Exception as e:
                logger.error(f"Error decoding text file: {str(e)}")
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to decode text file: {str(e)}"
                )

async def load_multimodal_data(files: List[UploadFile]) -> List[Document]:
    """Process multiple files of different types and return a list of Documents."""
    documents = []
    
    for file in files:
        content = await file.read()
        file_extension = os.path.splitext(file.filename)[1].lower()
        
        try:
            if file_extension in ['.pdf', '.txt', '.md', '.doc', '.docx']:
                text_content = await process_text_document(content, file_extension)
                doc = Document(
                    text=text_content,
                    metadata={
                        'source': file.filename,
                        'type': file_extension[1:],
                        'size': len(content)
                    }
                )
                documents.append(doc)
                
            elif file_extension in ['.png', '.jpg', '.jpeg']:
                if is_graph(content):
                    graph_text = process_graph(content)
                    doc = Document(
                        text=graph_text,
                        metadata={
                            'source': file.filename,
                            'type': 'graph',
                            'size': len(content)
                        }
                    )
                else:
                    image_text = describe_image(content)
                    doc = Document(
                        text=image_text,
                        metadata={
                            'source': file.filename,
                            'type': 'image',
                            'size': len(content)
                        }
                    )
                documents.append(doc)
                
        except Exception as e:
            logger.error(f"Error processing file {file.filename}: {str(e)}")
            continue
            
    return documents

def save_uploaded_file(uploaded_file: UploadFile) -> str:
    """Save an uploaded file to a temporary directory and return the file path."""
    temp_dir = os.path.join(os.getcwd(), "vectorstore", "ppt_references", "tmp")
    os.makedirs(temp_dir, exist_ok=True)
    temp_file_path = os.path.join(temp_dir, uploaded_file.filename)
    
    with open(temp_file_path, "wb") as temp_file:
        temp_file.write(uploaded_file.file.read())
    
    return temp_file_path