"""
AI-Powered Scam and Fraud Link Verifier
Configuration Settings

Copyright (c) 2025 Akash Kumar Singh
Email: meakash22dotin@gmail.com
GitHub: https://github.com/akashkumarsingh

This file is part of the AI-Powered Link Verifier project.
"""

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'AIzaSyDrusbKMinKP1ug8WliunH0iKYqyzmpC7I')
    GEMINI_API_KEY_2 = os.getenv('GEMINI_API_KEY_2', 'AIzaSyDrusbKMinKP1ug8WliunH0iKYqyzmpC7I')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
