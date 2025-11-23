"""
AI-Powered Scam and Fraud Link Verifier
Main Flask Application

Copyright (c) 2025 Akash Kumar Singh
Email: meakash22dotin@gmail.com
GitHub: https://github.com/akashkumarsingh

This file is part of the AI-Powered Link Verifier project.
"""

from flask import Flask, render_template, request, jsonify, send_file
import google.generativeai as genai
import requests
import validators
import tldextract
import json
import csv
import io
import base64
import qrcode
# import pythonwhois as whois  # Temporarily disabled due to compatibility issues
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from bs4 import BeautifulSoup
from PIL import Image
import hashlib
import re
from collections import defaultdict
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Configure Gemini API with multiple keys for redundancy
api_keys = [app.config['GEMINI_API_KEY'], app.config['GEMINI_API_KEY_2']]
current_api_key_index = 0

def get_current_api_key():
    global current_api_key_index
    return api_keys[current_api_key_index]

def switch_api_key():
    global current_api_key_index, model
    current_api_key_index = (current_api_key_index + 1) % len(api_keys)
    genai.configure(api_key=get_current_api_key())
    # Recreate the model with the new API key
    model = genai.GenerativeModel('gemini-2.5-flash')

# Initialize with first API key
genai.configure(api_key=get_current_api_key())
model = genai.GenerativeModel('gemini-2.5-flash')

class LinkAnalyzer:
    def __init__(self):
        self.suspicious_domains = [
            'bit.ly', 'tinyurl.com', 'short.link', 't.co', 'goo.gl',
            'ow.ly', 'is.gd', 'v.gd', 'shorturl.at'
        ]
        
        self.known_phishing_patterns = [
            'paypal-security', 'amazon-verification', 'microsoft-update',
            'apple-id', 'google-security', 'facebook-login', 'twitter-verify'
        ]
        
        # Advanced threat intelligence sources
        self.threat_intelligence_apis = {
            'virustotal': 'https://www.virustotal.com/vtapi/v2/url/report',
            'phishtank': 'https://checkurl.phishtank.com/checkurl/',
            'urlvoid': 'https://api.urlvoid.com/v1/pay-as-you-go/'
        }
        
        # Suspicious keywords for content analysis
        self.suspicious_keywords = [
            'urgent', 'verify', 'suspended', 'expired', 'security', 'update',
            'confirm', 'validate', 'restore', 'unlock', 'immediately'
        ]
        
        # Advanced threat intelligence
        self.threat_database = defaultdict(list)
        self.monitored_urls = {}
        self.threat_statistics = {
            'total_analyzed': 0,
            'safe_count': 0,
            'suspicious_count': 0,
            'malicious_count': 0,
            'threat_trends': []
        }
        
        # Email security patterns
        self.email_threat_patterns = [
            'verify your account', 'suspended account', 'urgent action required',
            'click here to verify', 'account security alert', 'immediate attention'
        ]
    
    def validate_url(self, url):
        """Validate if the URL is properly formatted"""
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        return validators.url(url)
    
    def extract_domain_info(self, url):
        """Extract domain information using tldextract"""
        extracted = tldextract.extract(url)
        return {
            'domain': f"{extracted.domain}.{extracted.suffix}",
            'subdomain': extracted.subdomain,
            'full_domain': f"{extracted.subdomain}.{extracted.domain}.{extracted.suffix}" if extracted.subdomain else f"{extracted.domain}.{extracted.suffix}"
        }
    
    def check_redirects(self, url):
        """Check for suspicious redirects"""
        try:
            response = requests.head(url, timeout=10, allow_redirects=True)
            redirect_count = len(response.history)
            final_url = response.url
            
            return {
                'redirect_count': redirect_count,
                'final_url': final_url,
                'suspicious_redirect': redirect_count > 3
            }
        except:
            return {'redirect_count': 0, 'final_url': url, 'suspicious_redirect': False}
    
    def analyze_domain_registration(self, domain):
        """Analyze domain registration information"""
        try:
            # Simplified domain analysis without whois for now
            # This can be enhanced with other domain analysis methods
            return {
                'creation_date': 'Unknown (WHOIS disabled)',
                'expiration_date': 'Unknown (WHOIS disabled)',
                'registrar': 'Unknown (WHOIS disabled)',
                'days_old': None,
                'is_recently_registered': False,
                'country': 'Unknown (WHOIS disabled)',
                'note': 'Domain registration analysis temporarily disabled'
            }
        except Exception as e:
            return {
                'creation_date': 'Unknown',
                'expiration_date': 'Unknown',
                'registrar': 'Unknown',
                'days_old': None,
                'is_recently_registered': False,
                'country': 'Unknown',
                'error': str(e)
            }
    
    def analyze_website_content(self, url):
        """Analyze website content for suspicious patterns"""
        try:
            response = requests.get(url, timeout=10, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract text content
            text_content = soup.get_text().lower()
            
            # Check for suspicious keywords
            suspicious_keyword_count = sum(1 for keyword in self.suspicious_keywords if keyword in text_content)
            
            # Check for forms (potential phishing)
            forms = soup.find_all('form')
            has_login_form = any('password' in str(form).lower() or 'login' in str(form).lower() for form in forms)
            
            # Check for external resources
            external_scripts = soup.find_all('script', src=True)
            external_links = soup.find_all('a', href=True)
            
            # Check for suspicious meta tags
            meta_tags = soup.find_all('meta')
            suspicious_meta = any('phishing' in str(meta).lower() or 'scam' in str(meta).lower() for meta in meta_tags)
            
            return {
                'suspicious_keyword_count': suspicious_keyword_count,
                'has_login_form': has_login_form,
                'external_scripts_count': len(external_scripts),
                'external_links_count': len(external_links),
                'suspicious_meta_tags': suspicious_meta,
                'content_length': len(text_content),
                'title': soup.title.string if soup.title else 'No title'
            }
        except Exception as e:
            return {
                'suspicious_keyword_count': 0,
                'has_login_form': False,
                'external_scripts_count': 0,
                'external_links_count': 0,
                'suspicious_meta_tags': False,
                'content_length': 0,
                'title': 'Error loading content',
                'error': str(e)
            }
    
    def generate_url_hash(self, url):
        """Generate hash for URL fingerprinting"""
        return hashlib.md5(url.encode()).hexdigest()
    
    def check_url_shortening_services(self, url):
        """Check if URL is from known shortening services"""
        shorteners = [
            'bit.ly', 'tinyurl.com', 'short.link', 't.co', 'goo.gl',
            'ow.ly', 'is.gd', 'v.gd', 'shorturl.at', 'rebrand.ly',
            'cutt.ly', 'short.ly', 'tiny.cc', 'buff.ly'
        ]
        
        domain = tldextract.extract(url).domain + '.' + tldextract.extract(url).suffix
        return domain in shorteners
    
    def analyze_url_structure(self, url):
        """Analyze URL structure for suspicious patterns"""
        # Check for suspicious characters
        suspicious_chars = ['@', '\\', '//', '..']
        has_suspicious_chars = any(char in url for char in suspicious_chars)
        
        # Check for IP address instead of domain
        ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
        has_ip_address = bool(re.search(ip_pattern, url))
        
        # Check for excessive subdomains
        parts = url.split('.')
        subdomain_count = len(parts) - 2  # Subtract domain and TLD
        
        # Check for typosquatting patterns
        common_typos = ['goggle', 'facebok', 'twiter', 'amazom', 'paypall']
        has_typo = any(typo in url.lower() for typo in common_typos)
        
        return {
            'has_suspicious_chars': has_suspicious_chars,
            'has_ip_address': has_ip_address,
            'subdomain_count': subdomain_count,
            'has_typosquatting': has_typo,
            'url_length': len(url)
        }
    
    def analyze_email_security(self, email_content):
        """Analyze email content for phishing patterns"""
        email_lower = email_content.lower()
        
        # Check for suspicious patterns
        suspicious_pattern_count = sum(1 for pattern in self.email_threat_patterns if pattern in email_lower)
        
        # Check for urgency indicators
        urgency_words = ['urgent', 'immediately', 'asap', 'critical', 'emergency']
        urgency_count = sum(1 for word in urgency_words if word in email_lower)
        
        # Check for action requests
        action_words = ['click', 'verify', 'confirm', 'update', 'validate']
        action_count = sum(1 for word in action_words if word in email_lower)
        
        # Calculate email threat score
        email_threat_score = (suspicious_pattern_count * 20) + (urgency_count * 10) + (action_count * 5)
        email_threat_score = min(email_threat_score, 100)
        
        return {
            'suspicious_patterns': suspicious_pattern_count,
            'urgency_indicators': urgency_count,
            'action_requests': action_count,
            'email_threat_score': email_threat_score,
            'is_likely_phishing': email_threat_score > 50
        }
    
    def get_threat_statistics(self):
        """Get comprehensive threat statistics"""
        total = self.threat_statistics['total_analyzed']
        if total == 0:
            return self.threat_statistics
        
        return {
            **self.threat_statistics,
            'safe_percentage': (self.threat_statistics['safe_count'] / total) * 100,
            'suspicious_percentage': (self.threat_statistics['suspicious_count'] / total) * 100,
            'malicious_percentage': (self.threat_statistics['malicious_count'] / total) * 100
        }
    
    def add_to_threat_database(self, url, analysis_result):
        """Add analysis result to threat database"""
        url_hash = self.generate_url_hash(url)
        self.threat_database[url_hash].append({
            'timestamp': datetime.now().isoformat(),
            'result': analysis_result
        })
        
        # Update statistics
        self.threat_statistics['total_analyzed'] += 1
        verdict = analysis_result.get('verdict', '').lower()
        if verdict == 'safe':
            self.threat_statistics['safe_count'] += 1
        elif verdict == 'suspicious':
            self.threat_statistics['suspicious_count'] += 1
        elif verdict == 'malicious':
            self.threat_statistics['malicious_count'] += 1
    
    def get_url_history(self, url):
        """Get analysis history for a URL"""
        url_hash = self.generate_url_hash(url)
        return self.threat_database.get(url_hash, [])
    
    def start_url_monitoring(self, url, interval_hours=24):
        """Start monitoring a URL for changes"""
        self.monitored_urls[url] = {
            'interval_hours': interval_hours,
            'last_checked': datetime.now(),
            'status': 'monitoring'
        }
    
    def stop_url_monitoring(self, url):
        """Stop monitoring a URL"""
        if url in self.monitored_urls:
            del self.monitored_urls[url]
    
    def get_monitored_urls(self):
        """Get list of currently monitored URLs"""
        return list(self.monitored_urls.keys())
    
    def analyze_network_security(self, ip_address):
        """Analyze network security for IP address"""
        try:
            # Check if IP is in private range
            import ipaddress
            ip = ipaddress.ip_address(ip_address)
            is_private = ip.is_private
            
            # Check for suspicious IP patterns
            suspicious_patterns = [
                ip_address.startswith('192.168.'),
                ip_address.startswith('10.'),
                ip_address.startswith('172.'),
                ip_address == '127.0.0.1'
            ]
            
            return {
                'ip_address': ip_address,
                'is_private': is_private,
                'is_localhost': ip_address == '127.0.0.1',
                'is_suspicious': any(suspicious_patterns),
                'network_type': 'private' if is_private else 'public'
            }
        except:
            return {
                'ip_address': ip_address,
                'is_private': False,
                'is_localhost': False,
                'is_suspicious': False,
                'network_type': 'unknown'
            }
    
    def analyze_with_ai(self, url, domain_info, redirect_info):
        """Use Gemini AI to analyze the link for potential threats"""
        prompt = f"""
        Analyze this URL for potential security threats, scams, or fraud:
        
        URL: {url}
        Domain: {domain_info['domain']}
        Subdomain: {domain_info['subdomain']}
        Redirects: {redirect_info['redirect_count']}
        Final URL: {redirect_info['final_url']}
        
        Please provide:
        1. A verdict: "Safe", "Suspicious", or "Malicious"
        2. A confidence score (0-100%)
        3. A brief explanation of your reasoning
        4. Specific threats detected (if any)
        
        Focus on:
        - Phishing patterns
        - Suspicious domain characteristics
        - Typosquatting
        - Malware indicators
        - Social engineering attempts
        
        Respond in JSON format:
        {{
            "verdict": "Safe/Suspicious/Malicious",
            "confidence": 85,
            "explanation": "Brief explanation here",
            "threats_detected": ["threat1", "threat2"]
        }}
        """
        
        # Try with current API key, switch to backup if needed
        max_retries = len(api_keys)
        for attempt in range(max_retries):
            try:
                response = model.generate_content(prompt)
                # Extract JSON from response
                response_text = response.text
                if '```json' in response_text:
                    json_start = response_text.find('```json') + 7
                    json_end = response_text.find('```', json_start)
                    json_text = response_text[json_start:json_end].strip()
                elif '{' in response_text and '}' in response_text:
                    json_start = response_text.find('{')
                    json_end = response_text.rfind('}') + 1
                    json_text = response_text[json_start:json_end]
                else:
                    json_text = response_text
                
                return json.loads(json_text)
            except json.JSONDecodeError as e:
                # If JSON parsing fails, try to extract verdict from text
                response_text = response.text if 'response' in locals() else "No response"
                if "safe" in response_text.lower():
                    verdict = "Safe"
                    confidence = 70
                elif "malicious" in response_text.lower():
                    verdict = "Malicious"
                    confidence = 80
                else:
                    verdict = "Suspicious"
                    confidence = 60
                
                return {
                    "verdict": verdict,
                    "confidence": confidence,
                    "explanation": f"AI analysis completed but JSON parsing failed. Raw response: {response_text[:200]}...",
                    "threats_detected": ["JSON Parse Error"]
                }
            except Exception as e:
                if attempt < max_retries - 1:
                    # Switch to backup API key
                    switch_api_key()
                    print(f"Switched to backup API key (attempt {attempt + 1})")
                    continue
                else:
                    # All API keys failed
                    return {
                        "verdict": "Suspicious",
                        "confidence": 50,
                        "explanation": f"AI analysis failed: {str(e)}",
                        "threats_detected": ["Analysis Error"]
                    }
        
        # If we get here, all API keys failed
        return {
            "verdict": "Suspicious",
            "confidence": 50,
            "explanation": "All API keys failed",
            "threats_detected": ["API Error"]
        }
    
    def analyze_link(self, url):
        """Main analysis function with advanced features"""
        # Validate URL
        if not self.validate_url(url):
            return {
                "url": url,
                "verdict": "Malicious",
                "confidence": 100,
                "explanation": "Invalid URL format",
                "threats_detected": ["Invalid URL"],
                "domain_info": {},
                "redirect_info": {},
                "timestamp": datetime.now().isoformat()
            }
        
        # Extract domain information
        domain_info = self.extract_domain_info(url)
        
        # Check redirects
        redirect_info = self.check_redirects(url)
        
        # Advanced analysis
        domain_registration = self.analyze_domain_registration(domain_info['domain'])
        url_structure = self.analyze_url_structure(url)
        is_shortener = self.check_url_shortening_services(url)
        url_hash = self.generate_url_hash(url)
        
        # Content analysis (only for accessible URLs)
        content_analysis = {}
        try:
            content_analysis = self.analyze_website_content(url)
        except:
            content_analysis = {"error": "Content analysis failed"}
        
        # Basic checks
        basic_checks = {
            "suspicious_domain": domain_info['domain'] in self.suspicious_domains,
            "phishing_pattern": any(pattern in url.lower() for pattern in self.known_phishing_patterns),
            "suspicious_redirect": redirect_info['suspicious_redirect'],
            "is_shortener": is_shortener,
            "recently_registered": domain_registration.get('is_recently_registered', False),
            "has_suspicious_chars": url_structure.get('has_suspicious_chars', False),
            "has_ip_address": url_structure.get('has_ip_address', False),
            "has_typosquatting": url_structure.get('has_typosquatting', False)
        }
        
        # AI Analysis with enhanced context
        ai_result = self.analyze_with_ai(url, domain_info, redirect_info)
        
        # Combine results
        result = {
            "url": url,
            "verdict": ai_result.get("verdict", "Suspicious"),
            "confidence": ai_result.get("confidence", 50),
            "explanation": ai_result.get("explanation", "Analysis completed"),
            "threats_detected": ai_result.get("threats_detected", []),
            "domain_info": domain_info,
            "redirect_info": redirect_info,
            "domain_registration": domain_registration,
            "url_structure": url_structure,
            "content_analysis": content_analysis,
            "basic_checks": basic_checks,
            "url_hash": url_hash,
            "timestamp": datetime.now().isoformat()
        }
        
        # Add to threat database and update statistics
        self.add_to_threat_database(url, result)
        
        return result

# Initialize analyzer
analyzer = LinkAnalyzer()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/debug/models')
def debug_models():
    """Debug endpoint to list available Gemini models"""
    try:
        models = genai.list_models()
        available_models = []
        for model in models:
            if 'generateContent' in model.supported_generation_methods:
                available_models.append({
                    'name': model.name,
                    'display_name': model.display_name,
                    'supported_methods': list(model.supported_generation_methods)
                })
        return jsonify({
            'status': 'success',
            'available_models': available_models,
            'total_models': len(available_models)
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500

@app.route('/api/status', methods=['GET'])
def api_status():
    """Get API key status and system information"""
    try:
        return jsonify({
            'status': 'success',
            'api_keys': {
                'total_keys': len(api_keys),
                'current_key_index': current_api_key_index,
                'current_key_preview': get_current_api_key()[:10] + '...',
                'backup_available': len(api_keys) > 1
            },
            'system': {
                'model': 'gemini-2.5-flash',
                'uptime': 'Active',
                'features': [
                    'AI Analysis', 'Domain Analysis', 'Content Analysis',
                    'QR Code Generation', 'Threat Intelligence', 'Bulk Analysis',
                    'PDF Export', 'CSV Export', 'API Redundancy'
                ]
            }
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500

@app.route('/analyze', methods=['POST'])
def analyze_single():
    data = request.get_json()
    url = data.get('url', '').strip()
    
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    
    try:
        result = analyzer.analyze_link(url)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

@app.route('/analyze_batch', methods=['POST'])
def analyze_batch():
    data = request.get_json()
    urls = data.get('urls', [])
    
    if not urls or not isinstance(urls, list):
        return jsonify({'error': 'URLs list is required'}), 400
    
    if len(urls) > 50:  # Limit batch size
        return jsonify({'error': 'Maximum 50 URLs allowed per batch'}), 400
    
    results = []
    for url in urls:
        try:
            result = analyzer.analyze_link(url.strip())
            results.append(result)
        except Exception as e:
            results.append({
                "url": url,
                "verdict": "Error",
                "confidence": 0,
                "explanation": f"Analysis failed: {str(e)}",
                "threats_detected": ["Analysis Error"],
                "timestamp": datetime.now().isoformat()
            })
    
    return jsonify({'results': results})

@app.route('/export_csv', methods=['POST'])
def export_csv():
    data = request.get_json()
    results = data.get('results', [])
    
    if not results:
        return jsonify({'error': 'No results to export'}), 400
    
    # Create CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow(['URL', 'Verdict', 'Confidence', 'Explanation', 'Threats', 'Timestamp'])
    
    # Write data
    for result in results:
        threats = ', '.join(result.get('threats_detected', []))
        writer.writerow([
            result.get('url', ''),
            result.get('verdict', ''),
            result.get('confidence', 0),
            result.get('explanation', ''),
            threats,
            result.get('timestamp', '')
        ])
    
    # Create response
    output.seek(0)
    csv_data = output.getvalue()
    output.close()
    
    # Return as downloadable file
    return send_file(
        io.BytesIO(csv_data.encode()),
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'link_analysis_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    )

@app.route('/export_pdf', methods=['POST'])
def export_pdf():
    data = request.get_json()
    results = data.get('results', [])
    
    if not results:
        return jsonify({'error': 'No results to export'}), 400
    
    # Create PDF in memory
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Title
    title = Paragraph("Advanced Link Analysis Report", styles['Title'])
    story.append(title)
    story.append(Spacer(1, 12))
    
    # Add results
    for i, result in enumerate(results, 1):
        story.append(Paragraph(f"<b>Link {i}:</b> {result.get('url', '')}", styles['Heading2']))
        story.append(Paragraph(f"<b>Verdict:</b> {result.get('verdict', '')}", styles['Normal']))
        story.append(Paragraph(f"<b>Confidence:</b> {result.get('confidence', 0)}%", styles['Normal']))
        story.append(Paragraph(f"<b>Explanation:</b> {result.get('explanation', '')}", styles['Normal']))
        
        # Add advanced analysis details
        if 'domain_registration' in result:
            reg_info = result['domain_registration']
            story.append(Paragraph(f"<b>Domain Age:</b> {reg_info.get('days_old', 'Unknown')} days", styles['Normal']))
            story.append(Paragraph(f"<b>Registrar:</b> {reg_info.get('registrar', 'Unknown')}", styles['Normal']))
        
        if 'url_structure' in result:
            struct_info = result['url_structure']
            story.append(Paragraph(f"<b>URL Length:</b> {struct_info.get('url_length', 0)} characters", styles['Normal']))
            story.append(Paragraph(f"<b>Subdomains:</b> {struct_info.get('subdomain_count', 0)}", styles['Normal']))
        
        threats = result.get('threats_detected', [])
        if threats:
            story.append(Paragraph(f"<b>Threats:</b> {', '.join(threats)}", styles['Normal']))
        
        story.append(Spacer(1, 12))
    
    doc.build(story)
    buffer.seek(0)
    
    return send_file(
        buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f'advanced_link_analysis_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
    )

@app.route('/generate_qr', methods=['POST'])
def generate_qr():
    """Generate QR code for a URL"""
    data = request.get_json()
    url = data.get('url', '').strip()
    
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    
    try:
        # Generate QR code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(url)
        qr.make(fit=True)
        
        # Create image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to base64
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        img_base64 = base64.b64encode(buffer.getvalue()).decode()
        
        return jsonify({
            'success': True,
            'qr_code': f'data:image/png;base64,{img_base64}',
            'url': url
        })
    except Exception as e:
        return jsonify({'error': f'QR code generation failed: {str(e)}'}), 500

@app.route('/analyze_qr', methods=['POST'])
def analyze_qr():
    """Analyze URL from QR code"""
    data = request.get_json()
    url = data.get('url', '').strip()
    
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    
    try:
        # Analyze the URL
        result = analyzer.analyze_link(url)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': f'QR analysis failed: {str(e)}'}), 500

@app.route('/threat_intelligence', methods=['POST'])
def threat_intelligence():
    """Get threat intelligence for a domain"""
    data = request.get_json()
    url = data.get('url', '').strip()
    
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    
    try:
        domain_info = analyzer.extract_domain_info(url)
        domain = domain_info['domain']
        
        # Get domain registration info
        registration_info = analyzer.analyze_domain_registration(domain)
        
        # Get URL structure analysis
        structure_info = analyzer.analyze_url_structure(url)
        
        # Generate threat score
        threat_score = 0
        if registration_info.get('is_recently_registered'):
            threat_score += 30
        if structure_info.get('has_suspicious_chars'):
            threat_score += 20
        if structure_info.get('has_ip_address'):
            threat_score += 25
        if structure_info.get('has_typosquatting'):
            threat_score += 35
        
        return jsonify({
            'status': 'success',
            'result': {
                'url': url,
                'domain': domain,
                'threat_score': min(threat_score, 100),
                'risk_level': 'Low' if threat_score < 30 else 'Medium' if threat_score < 70 else 'High',
                'threats_detected': [],
                'registration_info': registration_info,
                'structure_info': structure_info,
                'url_hash': analyzer.generate_url_hash(url),
                'timestamp': datetime.now().isoformat()
            }
        })
    except Exception as e:
        return jsonify({'error': f'Threat intelligence failed: {str(e)}'}), 500

@app.route('/bulk_analyze', methods=['POST'])
def bulk_analyze():
    """Bulk analyze multiple URLs with advanced features"""
    data = request.get_json()
    urls = data.get('urls', [])
    
    if not urls or not isinstance(urls, list):
        return jsonify({'error': 'URLs list is required'}), 400
    
    if len(urls) > 100:  # Increased limit for bulk analysis
        return jsonify({'error': 'Maximum 100 URLs allowed per bulk analysis'}), 400
    
    results = []
    for url in urls:
        try:
            result = analyzer.analyze_link(url.strip())
            results.append(result)
        except Exception as e:
            results.append({
                "url": url,
                "verdict": "Error",
                "confidence": 0,
                "explanation": f"Analysis failed: {str(e)}",
                "threats_detected": ["Analysis Error"],
                "timestamp": datetime.now().isoformat()
            })
    
    # Generate summary statistics
    verdict_counts = {}
    for result in results:
        verdict = result.get('verdict', 'Unknown')
        verdict_counts[verdict] = verdict_counts.get(verdict, 0) + 1
    
    return jsonify({
        'results': results,
        'summary': {
            'total_urls': len(urls),
            'successful_analyses': len([r for r in results if r.get('verdict') != 'Error']),
            'verdict_distribution': verdict_counts,
            'average_confidence': sum(r.get('confidence', 0) for r in results) / len(results) if results else 0
        }
    })

@app.route('/email_analysis', methods=['POST'])
def analyze_email():
    """Analyze email content for phishing patterns"""
    data = request.get_json()
    email_content = data.get('email_content', '').strip()
    
    if not email_content:
        return jsonify({'error': 'Email content is required'}), 400
    
    try:
        result = analyzer.analyze_email_security(email_content)
        return jsonify({
            'email_analysis': result,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': f'Email analysis failed: {str(e)}'}), 500

@app.route('/threat_statistics', methods=['GET'])
def get_threat_statistics():
    """Get comprehensive threat statistics"""
    try:
        stats = analyzer.get_threat_statistics()
        return jsonify({
            'statistics': stats,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': f'Failed to get statistics: {str(e)}'}), 500

@app.route('/url_history/<path:url>', methods=['GET'])
def get_url_history(url):
    """Get analysis history for a specific URL"""
    try:
        history = analyzer.get_url_history(url)
        return jsonify({
            'url': url,
            'history': history,
            'total_analyses': len(history),
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': f'Failed to get URL history: {str(e)}'}), 500

@app.route('/monitor_url', methods=['POST'])
def monitor_url():
    """Start monitoring a URL for changes"""
    data = request.get_json()
    url = data.get('url', '').strip()
    interval_hours = data.get('interval_hours', 24)
    
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    
    try:
        analyzer.start_url_monitoring(url, interval_hours)
        return jsonify({
            'message': f'Started monitoring {url}',
            'interval_hours': interval_hours,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': f'Failed to start monitoring: {str(e)}'}), 500

@app.route('/stop_monitoring', methods=['POST'])
def stop_monitoring():
    """Stop monitoring a URL"""
    data = request.get_json()
    url = data.get('url', '').strip()
    
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    
    try:
        analyzer.stop_url_monitoring(url)
        return jsonify({
            'message': f'Stopped monitoring {url}',
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': f'Failed to stop monitoring: {str(e)}'}), 500

@app.route('/monitored_urls', methods=['GET'])
def get_monitored_urls():
    """Get list of currently monitored URLs"""
    try:
        monitored = analyzer.get_monitored_urls()
        return jsonify({
            'monitored_urls': monitored,
            'count': len(monitored),
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': f'Failed to get monitored URLs: {str(e)}'}), 500

@app.route('/network_analysis', methods=['POST'])
def analyze_network():
    """Analyze network security for IP address"""
    data = request.get_json()
    ip_address = data.get('ip_address', '').strip()
    
    if not ip_address:
        return jsonify({'error': 'IP address is required'}), 400
    
    try:
        result = analyzer.analyze_network_security(ip_address)
        return jsonify({
            'network_analysis': result,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': f'Network analysis failed: {str(e)}'}), 500

@app.route('/threat_dashboard', methods=['GET'])
def threat_dashboard():
    """Get comprehensive threat dashboard data"""
    try:
        stats = analyzer.get_threat_statistics()
        monitored = analyzer.get_monitored_urls()
        
        return jsonify({
            'dashboard': {
                'statistics': stats,
                'monitored_urls': monitored,
                'total_monitored': len(monitored),
                'system_status': 'operational'
            },
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': f'Failed to get dashboard data: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=app.config['FLASK_DEBUG'], host='0.0.0.0', port=5001)
