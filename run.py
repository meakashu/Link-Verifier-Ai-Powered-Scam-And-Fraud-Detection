#!/usr/bin/env python3
"""
AI-Powered Scam and Fraud Link Verifier
Application Runner Script

Copyright (c) 2025 Akash Kumar Singh
Email: meakash22dotin@gmail.com
GitHub: https://github.com/akashkumarsingh

This script provides an easy way to start the application with proper configuration.
"""

import os
import sys
from app import app

def main():
    """Main function to run the application."""
    print("🚀 Starting AI-Powered Link Verifier...")
    print("📱 Web interface will be available at: http://localhost:5001")
    print("🔒 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        # Run the Flask application
        app.run(
            debug=app.config['FLASK_DEBUG'],
            host='0.0.0.0',
            port=5001,
            threaded=True
        )
    except KeyboardInterrupt:
        print("\n👋 Shutting down the server...")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
