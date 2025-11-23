# 🛡️ AI-Powered Scam and Fraud Link Verifier

<div align="center">

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![GitHub stars](https://img.shields.io/github/stars/yourusername/link-verifier?style=social)

**A comprehensive AI-powered web application for detecting malicious URLs, phishing attempts, and fraudulent links using Google Gemini AI**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [API Documentation](#-api-documentation) • [Contributing](#-contributing) • [License](#-license)

## 📋 Demo: (https://link-verifier-ai-powered-scam-and-f.vercel.app/)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Technology Stack](#-technology-stack)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [API Documentation](#-api-documentation)
- [Project Structure](#-project-structure)
- [Security](#-security)
- [Contributing](#-contributing)
- [License](#-license)
- [Support](#-support)

---

## 🎯 Overview

The **AI-Powered Scam and Fraud Link Verifier** is an advanced cybersecurity tool that leverages Google's Gemini AI to analyze URLs for potential security threats. Unlike traditional binary safe/unsafe classification systems, this application provides intelligent threat detection with detailed explanations, confidence scores, and comprehensive analysis across multiple attack vectors.

### Key Highlights

- 🤖 **AI-Powered Analysis**: Uses Google Gemini 2.5 Flash for intelligent threat detection
- 🔍 **Multi-Layer Detection**: Identifies phishing, malware, typosquatting, and suspicious patterns
- 📊 **Confidence Scoring**: Provides 0-100% confidence scores for each analysis
- 📦 **Batch Processing**: Analyze up to 100 URLs simultaneously
- 📄 **Professional Reports**: Export results as CSV or PDF
- 🔐 **Secure Analysis**: No auto-clicking or executing links - safe analysis only
- 📱 **Responsive Design**: Modern, mobile-friendly interface
- ⚡ **Real-Time Processing**: Fast analysis with sub-2-second response times

---

## 🚀 Features

### Core Functionality

- **Single Link Analysis**: Analyze individual URLs with detailed threat assessment
- **Batch Processing**: Process up to 100 URLs simultaneously with progress tracking
- **AI-Powered Detection**: Intelligent threat analysis using Google Gemini AI
- **Multiple Threat Detection**: Identifies phishing, malware, typosquatting, and suspicious patterns
- **Confidence Scoring**: Provides 0-100% confidence scores for each analysis
- **Natural Language Explanations**: Detailed explanations of detected threats

### Advanced Features

- **QR Code Analysis**: Generate and analyze QR codes for mobile security
- **Threat Intelligence**: Comprehensive domain and URL structure analysis
- **Email Security Analysis**: Detect phishing patterns in email content
- **URL Monitoring**: Continuous monitoring of URLs for changes
- **Threat Dashboard**: Real-time analytics and statistics
- **Analysis History**: Local storage of analysis history
- **Export Capabilities**: Export results as CSV or PDF reports
- **Domain Analysis**: Detailed domain, subdomain, and TLD information
- **Redirect Detection**: Identifies suspicious redirect chains

### Security Features

- ✅ **Safe Analysis**: No auto-clicking, downloading, or executing links
- ✅ **URL Validation**: Comprehensive URL format validation
- ✅ **Threat Intelligence**: Cross-references with known patterns
- ✅ **Secure Processing**: All analysis performed server-side
- ✅ **Input Sanitization**: Comprehensive input validation and sanitization

---

## 🛠️ Technology Stack

### Backend
- **Python 3.7+**: Core programming language
- **Flask 2.3.3**: Web framework
- **Google Gemini AI**: AI-powered threat analysis
- **BeautifulSoup4**: HTML content parsing
- **ReportLab**: PDF report generation
- **tldextract**: Domain extraction and analysis
- **validators**: URL validation

### Frontend
- **Bootstrap 5**: Responsive UI framework
- **Vanilla JavaScript**: Frontend logic
- **Font Awesome**: Icon library
- **LocalStorage API**: Client-side data storage

### AI & Analysis
- **Google Gemini 2.5 Flash**: AI model for threat detection
- **Pattern Matching**: Known threat pattern detection
- **Content Analysis**: Website content scanning
- **Domain Intelligence**: Domain registration and structure analysis

---

## 📦 Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

### Step 1: Clone the Repository

```bash
git clone https://github.com/akashkumarsingh/link-verifier.git
cd link-verifier
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure API Key

Create a `.env` file in the project root:

```bash
# .env
GEMINI_API_KEY=your_api_key_here
GEMINI_API_KEY_2=your_backup_api_key_here  # Optional
FLASK_ENV=development
FLASK_DEBUG=True
```

Alternatively, you can edit `config.py` directly (not recommended for production).

### Step 5: Run the Application

```bash
# Using run.py
python run.py

# Or directly
python app.py
```

The application will start on `http://localhost:5001`

---

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GEMINI_API_KEY` | Primary Google Gemini API key | Required |
| `GEMINI_API_KEY_2` | Backup API key for redundancy | Optional |
| `FLASK_ENV` | Flask environment | `development` |
| `FLASK_DEBUG` | Enable debug mode | `True` |

### Application Settings

Edit `config.py` to customize:
- API keys
- Flask configuration
- Debug settings

---

## 🎯 Usage

### Web Interface

1. Open `http://localhost:5001` in your browser
2. Navigate to the desired tab:
   - **Single Link**: Analyze individual URLs
   - **Batch Analysis**: Process multiple URLs
   - **QR Code**: Generate and analyze QR codes
   - **Threat Intel**: Get comprehensive threat intelligence
   - **Email Analysis**: Analyze email content for phishing
   - **URL Monitoring**: Monitor URLs for changes
   - **Dashboard**: View analytics and statistics
   - **History**: View analysis history

### Single Link Analysis

1. Navigate to "Single Link" tab
2. Enter the URL you want to analyze
3. Click "Analyze"
4. Review the verdict, confidence score, and detailed explanation

### Batch Analysis

1. Go to "Batch Analysis" tab
2. Enter multiple URLs (one per line, up to 100 URLs)
3. Click "Analyze All"
4. Review results for each URL
5. Export results as CSV or PDF if needed

### API Usage

See [API Documentation](#-api-documentation) for detailed API endpoint information.

---

## 📚 API Documentation

### Base URL
```
http://localhost:5001
```

### Endpoints

#### Analyze Single Link
```http
POST /analyze
Content-Type: application/json

{
    "url": "https://example.com"
}
```

**Response:**
```json
{
    "url": "https://example.com",
    "verdict": "Safe",
    "confidence": 95,
    "explanation": "The URL appears to be legitimate...",
    "threats_detected": [],
    "domain_info": {...},
    "timestamp": "2025-01-01T12:00:00"
}
```

#### Batch Analysis
```http
POST /analyze_batch
Content-Type: application/json

{
    "urls": ["https://example1.com", "https://example2.com"]
}
```

#### Export CSV
```http
POST /export_csv
Content-Type: application/json

{
    "results": [/* analysis results array */]
}
```

#### Export PDF
```http
POST /export_pdf
Content-Type: application/json

{
    "results": [/* analysis results array */]
}
```

#### Threat Intelligence
```http
POST /threat_intelligence
Content-Type: application/json

{
    "url": "https://example.com"
}
```

#### Email Analysis
```http
POST /email_analysis
Content-Type: application/json

{
    "email_content": "Email content here..."
}
```

#### Get Threat Statistics
```http
GET /threat_statistics
```

#### Get API Status
```http
GET /api/status
```

For complete API documentation, see the [API Documentation](docs/API.md) file.

---

## 📁 Project Structure

```
link-verifier/
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── run.py                 # Application runner script
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── LICENSE               # License file
├── CONTRIBUTING.md       # Contribution guidelines
├── .gitignore            # Git ignore rules
├── .env                  # Environment variables (create this)
├── templates/
│   └── index.html       # Main web interface
├── static/
│   ├── css/
│   │   └── style.css    # Custom styling
│   └── js/
│       └── app.js       # Frontend JavaScript
├── Project Report/
│   ├── Project_Report.md
│   └── README.md
└── Week Report/
    ├── README.md
    └── WPR_*.md
```

---

## 🔒 Security

### What This Tool Does

- ✅ Analyzes URL structure and patterns
- ✅ Checks domain reputation
- ✅ Detects suspicious redirects
- ✅ Uses AI for threat intelligence
- ✅ Provides detailed security reports
- ✅ Validates URL format

### What This Tool Does NOT Do

- ❌ Visit or execute the analyzed URLs
- ❌ Download files from suspicious links
- ❌ Auto-click on any links
- ❌ Store personal information
- ❌ Share data with third parties
- ❌ Make security decisions for you

### Security Best Practices

1. **Keep API Keys Secure**: Never commit API keys to version control
2. **Use Environment Variables**: Store sensitive data in `.env` files
3. **Regular Updates**: Keep dependencies updated
4. **Input Validation**: All inputs are validated and sanitized
5. **HTTPS in Production**: Always use HTTPS in production environments

### Important Disclaimer

This tool is for **educational and informational purposes only**. Results should not be the sole basis for security decisions. Always use additional security measures and common sense. The AI may occasionally produce false positives or negatives.

---

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Contribution Guidelines

- Follow PEP 8 style guidelines
- Write clear commit messages
- Add tests for new features
- Update documentation as needed
- Ensure all tests pass

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🆘 Support

### Getting Help

- 📖 Check the [Documentation](docs/)
- 🐛 [Open an Issue](https://github.com/akashkumarsingh/link-verifier/issues)
- 💬 [Start a Discussion](https://github.com/akashkumarsingh/link-verifier/discussions)
- 📧 Contact: [meakash22dotin@gmail.com](mailto:meakash22dotin@gmail.com)

### Troubleshooting

**API Errors**
- Check your Gemini API key and quota
- Verify API key is correctly set in `.env` file
- Check network connectivity

**Installation Issues**
- Ensure Python 3.7+ is installed
- Use virtual environment
- Update pip: `pip install --upgrade pip`

**Analysis Failures**
- Some URLs may be unreachable or blocked
- Check URL format is correct
- Verify internet connection

---

## 👨‍💻 Author

**Akash Kumar Singh**

- 📧 Email: [meakash22dotin@gmail.com](mailto:meakash22dotin@gmail.com)
- 🌐 GitHub: [@akashkumarsingh](https://github.com/meakashu)
- 💼 LinkedIn: [Akash Kumar Singh](https://www.linkedin.com/authwall?trk=bf&trkInfo=AQEWFteNYuvbHgAAAZqxRe_w93jqNHNVgw9F1Dm71U8ymGS9OA_j31I852BAInjhljiN4Ti-Bmr_T9h5FXAflClmv4dE3T9-Ep5Hgv3JgvDFGR39MXfWBWJze_vnCQxmgZjWyf0=&original_referer=&sessionRedirect=https%3A%2F%2Fwww.linkedin.com%2Fin%2Fakash-kumar-singh-883377273%2F)

## 🌟 Acknowledgments

- [Google Gemini AI](https://ai.google.dev/) for AI capabilities
- [Flask](https://flask.palletsprojects.com/) for the web framework
- [Bootstrap](https://getbootstrap.com/) for UI components
- All contributors and users of this project

---

## 📊 Project Status

![GitHub last commit](https://img.shields.io/github/last-commit/akashkumarsingh/link-verifier)
![GitHub issues](https://img.shields.io/github/issues/akashkumarsingh/link-verifier)
![GitHub pull requests](https://img.shields.io/github/issues-pr/akashkumarsingh/link-verifier)

**Current Version**: 1.0.0  
**Status**: ✅ Production Ready  
**Maintenance**: Actively Maintained  
**Copyright**: © 2025 Akash Kumar Singh. All rights reserved.

---

<div align="center">

**Made with ❤️ by Akash Kumar Singh**

⭐ Star this repo if you find it helpful!

📧 Contact: [meakash22dotin@gmail.com](mailto:meakash22dotin@gmail.com)

[⬆ Back to Top](#-ai-powered-scam-and-fraud-link-verifier)

</div>

