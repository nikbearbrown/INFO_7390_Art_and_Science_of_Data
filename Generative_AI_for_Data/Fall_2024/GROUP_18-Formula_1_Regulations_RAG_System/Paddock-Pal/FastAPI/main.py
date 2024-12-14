
from fastapi import FastAPI, Depends
from jwtauth import router  # Ensure jwtauth.py has a `router` defined
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
import boto3
import os
from dotenv import load_dotenv
app = FastAPI()

# Include the `jwtauth.py` router
app.include_router(router, prefix="/auth")

# Define the OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Add CORS middleware if needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI JWT Authentication Application!"}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
