// Global variables
let analysisHistory = JSON.parse(localStorage.getItem('analysisHistory') || '[]');
let currentBatchResults = [];

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeEventListeners();
    loadHistory();
});

function initializeEventListeners() {
    // Single link form
    document.getElementById('single-form').addEventListener('submit', handleSingleAnalysis);
    
    // Batch form
    document.getElementById('batch-form').addEventListener('submit', handleBatchAnalysis);
    
    // QR code forms
    document.getElementById('qr-generate-form').addEventListener('submit', handleQRGenerate);
    document.getElementById('qr-analyze-form').addEventListener('submit', handleQRAnalyze);
    
    // Threat intelligence form
    document.getElementById('threat-form').addEventListener('submit', handleThreatIntelligence);
    
    // Email analysis form
    document.getElementById('email-form').addEventListener('submit', handleEmailAnalysis);
    
    // URL monitoring form
    document.getElementById('monitor-form').addEventListener('submit', handleURLMonitoring);
}

function showTab(tabName) {
    // Hide all tabs
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // Remove active class from all nav tabs
    document.querySelectorAll('.nav-tab').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // Show selected tab
    document.getElementById(tabName + '-tab').classList.add('active');
    
    // Add active class to clicked nav tab
    event.target.classList.add('active');
    
    // Load specific tab data
    if (tabName === 'history') {
        loadHistory();
    } else if (tabName === 'dashboard') {
        loadDashboard();
    } else if (tabName === 'monitor') {
        loadMonitoredURLs();
    }
}

async function handleSingleAnalysis(event) {
    event.preventDefault();
    
    const url = document.getElementById('single-url').value.trim();
    if (!url) {
        showAlert('Please enter a URL to analyze.', 'danger');
        return;
    }
    
    showLoadingModal();
    
    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url: url })
        });
        
        const result = await response.json();
        
        if (response.ok) {
            displaySingleResult(result);
            addToHistory(result);
        } else {
            showAlert(result.error || 'Analysis failed', 'danger');
        }
    } catch (error) {
        showAlert('Network error: ' + error.message, 'danger');
    } finally {
        hideLoadingModal();
    }
}

async function handleBatchAnalysis(event) {
    event.preventDefault();
    
    const urlsText = document.getElementById('batch-urls').value.trim();
    if (!urlsText) {
        showAlert('Please enter URLs to analyze.', 'danger');
        return;
    }
    
    const urls = urlsText.split('\n')
        .map(url => url.trim())
        .filter(url => url.length > 0);
    
    if (urls.length === 0) {
        showAlert('Please enter at least one valid URL.', 'danger');
        return;
    }
    
    if (urls.length > 50) {
        showAlert('Maximum 50 URLs allowed per batch.', 'danger');
        return;
    }
    
    showLoadingModal();
    
    try {
        const response = await fetch('/analyze_batch', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ urls: urls })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            currentBatchResults = data.results;
            displayBatchResults(data.results);
            addBatchToHistory(data.results);
        } else {
            showAlert(data.error || 'Batch analysis failed', 'danger');
        }
    } catch (error) {
        showAlert('Network error: ' + error.message, 'danger');
    } finally {
        hideLoadingModal();
    }
}

function displaySingleResult(result) {
    const resultContainer = document.getElementById('single-result');
    resultContainer.style.display = 'block';
    
    const verdictClass = result.verdict.toLowerCase();
    const confidence = result.confidence || 0;
    
    resultContainer.innerHTML = `
        <div class="result-verdict ${verdictClass}">
            <i class="fas ${getVerdictIcon(result.verdict)}"></i>
            <span>${result.verdict}</span>
        </div>
        
        <div class="confidence-section">
            <label>Confidence: ${confidence}%</label>
            <div class="confidence-bar">
                <div class="confidence-fill ${verdictClass}" style="width: ${confidence}%"></div>
            </div>
        </div>
        
        <div class="result-details">
            <h6><i class="fas fa-info-circle"></i> Analysis Details</h6>
            <p><strong>URL:</strong> <code>${result.url}</code></p>
            <p><strong>Explanation:</strong> ${result.explanation}</p>
            
            ${result.domain_info ? `
                <p><strong>Domain:</strong> ${result.domain_info.domain}</p>
                ${result.domain_info.subdomain ? `<p><strong>Subdomain:</strong> ${result.domain_info.subdomain}</p>` : ''}
            ` : ''}
            
            ${result.redirect_info ? `
                <p><strong>Redirects:</strong> ${result.redirect_info.redirect_count}</p>
                ${result.redirect_info.final_url !== result.url ? `<p><strong>Final URL:</strong> <code>${result.redirect_info.final_url}</code></p>` : ''}
            ` : ''}
            
            ${result.threats_detected && result.threats_detected.length > 0 ? `
                <h6><i class="fas fa-exclamation-triangle"></i> Threats Detected</h6>
                <ul class="threats-list">
                    ${result.threats_detected.map(threat => `<li><i class="fas fa-times-circle"></i> ${threat}</li>`).join('')}
                </ul>
            ` : ''}
            
            <p class="text-muted mt-3">
                <small><i class="fas fa-clock"></i> Analyzed on ${new Date(result.timestamp).toLocaleString()}</small>
            </p>
        </div>
    `;
}

function displayBatchResults(results) {
    const resultsContainer = document.getElementById('batch-results');
    const resultList = document.getElementById('batch-result-list');
    
    resultsContainer.style.display = 'block';
    
    resultList.innerHTML = results.map((result, index) => {
        const verdictClass = result.verdict.toLowerCase();
        const confidence = result.confidence || 0;
        
        return `
            <div class="result-item">
                <div class="result-item-header">
                    <div class="result-url">${result.url}</div>
                    <span class="result-badge ${verdictClass}">${result.verdict}</span>
                </div>
                
                <div class="confidence-section">
                    <label>Confidence: ${confidence}%</label>
                    <div class="confidence-bar">
                        <div class="confidence-fill ${verdictClass}" style="width: ${confidence}%"></div>
                    </div>
                </div>
                
                <p><strong>Explanation:</strong> ${result.explanation}</p>
                
                ${result.threats_detected && result.threats_detected.length > 0 ? `
                    <div class="threats-section">
                        <strong>Threats:</strong>
                        <ul class="threats-list">
                            ${result.threats_detected.map(threat => `<li><i class="fas fa-times-circle"></i> ${threat}</li>`).join('')}
                        </ul>
                    </div>
                ` : ''}
                
                <p class="text-muted mt-2">
                    <small><i class="fas fa-clock"></i> ${new Date(result.timestamp).toLocaleString()}</small>
                </p>
            </div>
        `;
    }).join('');
}

function getVerdictIcon(verdict) {
    switch (verdict.toLowerCase()) {
        case 'safe':
            return 'fa-check-circle';
        case 'suspicious':
            return 'fa-exclamation-triangle';
        case 'malicious':
            return 'fa-times-circle';
        default:
            return 'fa-question-circle';
    }
}

function addToHistory(result) {
    analysisHistory.unshift(result);
    if (analysisHistory.length > 100) {
        analysisHistory = analysisHistory.slice(0, 100);
    }
    localStorage.setItem('analysisHistory', JSON.stringify(analysisHistory));
}

function addBatchToHistory(results) {
    results.forEach(result => addToHistory(result));
}

function loadHistory() {
    const historyContent = document.getElementById('history-content');
    
    if (analysisHistory.length === 0) {
        historyContent.innerHTML = '<p class="text-muted">No analysis history available. Start analyzing links to see your history here.</p>';
        return;
    }
    
    historyContent.innerHTML = `
        <div class="d-flex justify-content-between align-items-center mb-3">
            <h5>Recent Analyses (${analysisHistory.length})</h5>
            <button class="btn btn-outline-danger btn-sm" onclick="clearHistory()">
                <i class="fas fa-trash"></i> Clear History
            </button>
        </div>
        <div class="history-list">
            ${analysisHistory.map(result => `
                <div class="result-item">
                    <div class="result-item-header">
                        <div class="result-url">${result.url}</div>
                        <span class="result-badge ${result.verdict.toLowerCase()}">${result.verdict}</span>
                    </div>
                    <p><strong>Confidence:</strong> ${result.confidence}%</p>
                    <p><strong>Explanation:</strong> ${result.explanation}</p>
                    <p class="text-muted">
                        <small><i class="fas fa-clock"></i> ${new Date(result.timestamp).toLocaleString()}</small>
                    </p>
                </div>
            `).join('')}
        </div>
    `;
}

function clearHistory() {
    if (confirm('Are you sure you want to clear all analysis history?')) {
        analysisHistory = [];
        localStorage.removeItem('analysisHistory');
        loadHistory();
    }
}

function clearBatch() {
    document.getElementById('batch-urls').value = '';
    document.getElementById('batch-results').style.display = 'none';
    currentBatchResults = [];
}

async function exportResults(format) {
    if (currentBatchResults.length === 0) {
        showAlert('No results to export. Please run a batch analysis first.', 'warning');
        return;
    }
    
    try {
        const response = await fetch(`/export_${format}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ results: currentBatchResults })
        });
        
        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `link_analysis_${new Date().toISOString().slice(0, 19).replace(/:/g, '-')}.${format}`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
            
            showAlert(`Results exported successfully as ${format.toUpperCase()}!`, 'success');
        } else {
            const error = await response.json();
            showAlert(error.error || 'Export failed', 'danger');
        }
    } catch (error) {
        showAlert('Export error: ' + error.message, 'danger');
    }
}

function showLoadingModal() {
    const modal = new bootstrap.Modal(document.getElementById('loadingModal'));
    modal.show();
}

function hideLoadingModal() {
    const modal = bootstrap.Modal.getInstance(document.getElementById('loadingModal'));
    if (modal) {
        modal.hide();
    }
}

function showAlert(message, type) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    // Insert at the top of the main content
    const mainContent = document.querySelector('.main-content');
    mainContent.insertBefore(alertDiv, mainContent.firstChild);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, 5000);
}

// Utility function to validate URL format
function isValidUrl(string) {
    try {
        new URL(string);
        return true;
    } catch (_) {
        return false;
    }
}

// QR Code Generation
async function handleQRGenerate(event) {
    event.preventDefault();
    
    const url = document.getElementById('qr-url').value.trim();
    if (!url) {
        showAlert('Please enter a URL to generate QR code.', 'danger');
        return;
    }
    
    showLoadingModal();
    
    try {
        const response = await fetch('/generate_qr', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url: url })
        });
        
        const result = await response.json();
        
        if (response.ok) {
            displayQRCode(result);
        } else {
            showAlert(result.error || 'QR code generation failed', 'danger');
        }
    } catch (error) {
        showAlert('Network error: ' + error.message, 'danger');
    } finally {
        hideLoadingModal();
    }
}

function displayQRCode(result) {
    const qrResult = document.getElementById('qr-result');
    qrResult.style.display = 'block';
    
    qrResult.innerHTML = `
        <div class="card">
            <div class="card-body text-center">
                <h6>QR Code for:</h6>
                <p class="text-muted"><code>${result.url}</code></p>
                <img src="${result.qr_code}" alt="QR Code" class="img-fluid" style="max-width: 200px;">
                <div class="mt-3">
                    <button class="btn btn-sm btn-outline-primary" onclick="downloadQRCode('${result.qr_code}', '${result.url}')">
                        <i class="fas fa-download"></i> Download QR Code
                    </button>
                </div>
            </div>
        </div>
    `;
}

function downloadQRCode(qrCodeData, url) {
    const link = document.createElement('a');
    link.href = qrCodeData;
    link.download = `qr_code_${url.replace(/[^a-zA-Z0-9]/g, '_')}.png`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// QR Code Analysis
async function handleQRAnalyze(event) {
    event.preventDefault();
    
    const url = document.getElementById('qr-analyze-url').value.trim();
    if (!url) {
        showAlert('Please enter a URL from QR code to analyze.', 'danger');
        return;
    }
    
    showLoadingModal();
    
    try {
        const response = await fetch('/analyze_qr', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url: url })
        });
        
        const result = await response.json();
        
        if (response.ok) {
            displayQRAnalysis(result);
        } else {
            showAlert(result.error || 'QR analysis failed', 'danger');
        }
    } catch (error) {
        showAlert('Network error: ' + error.message, 'danger');
    } finally {
        hideLoadingModal();
    }
}

function displayQRAnalysis(result) {
    const qrAnalysisResult = document.getElementById('qr-analysis-result');
    qrAnalysisResult.style.display = 'block';
    
    const verdictClass = result.verdict.toLowerCase();
    const confidence = result.confidence || 0;
    
    qrAnalysisResult.innerHTML = `
        <div class="result-verdict ${verdictClass}">
            <i class="fas ${getVerdictIcon(result.verdict)}"></i>
            <span>QR Code Analysis: ${result.verdict}</span>
        </div>
        
        <div class="confidence-section">
            <label>Confidence: ${confidence}%</label>
            <div class="confidence-bar">
                <div class="confidence-fill ${verdictClass}" style="width: ${confidence}%"></div>
            </div>
        </div>
        
        <div class="result-details">
            <h6><i class="fas fa-info-circle"></i> QR Code Analysis Details</h6>
            <p><strong>URL:</strong> <code>${result.url}</code></p>
            <p><strong>Explanation:</strong> ${result.explanation}</p>
            
            ${result.domain_info ? `
                <p><strong>Domain:</strong> ${result.domain_info.domain}</p>
                ${result.domain_info.subdomain ? `<p><strong>Subdomain:</strong> ${result.domain_info.subdomain}</p>` : ''}
            ` : ''}
            
            ${result.redirect_info ? `
                <p><strong>Redirects:</strong> ${result.redirect_info.redirect_count}</p>
                ${result.redirect_info.final_url !== result.url ? `<p><strong>Final URL:</strong> <code>${result.redirect_info.final_url}</code></p>` : ''}
            ` : ''}
            
            ${result.threats_detected && result.threats_detected.length > 0 ? `
                <h6><i class="fas fa-exclamation-triangle"></i> Threats Detected</h6>
                <ul class="threats-list">
                    ${result.threats_detected.map(threat => `<li><i class="fas fa-times-circle"></i> ${threat}</li>`).join('')}
                </ul>
            ` : ''}
            
            <p class="text-muted mt-3">
                <small><i class="fas fa-clock"></i> Analyzed on ${new Date(result.timestamp).toLocaleString()}</small>
            </p>
        </div>
    `;
}

// Threat Intelligence
async function handleThreatIntelligence(event) {
    event.preventDefault();
    
    const url = document.getElementById('threat-url').value.trim();
    if (!url) {
        showAlert('Please enter a URL for threat intelligence.', 'danger');
        return;
    }
    
    showLoadingModal();
    
    try {
        const response = await fetch('/threat_intelligence', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url: url })
        });
        
        const result = await response.json();
        
        if (response.ok) {
            displayThreatIntelligence(result);
        } else {
            showAlert(result.error || 'Threat intelligence failed', 'danger');
        }
    } catch (error) {
        showAlert('Network error: ' + error.message, 'danger');
    } finally {
        hideLoadingModal();
    }
}

function displayThreatIntelligence(result) {
    const threatResult = document.getElementById('threat-result');
    threatResult.style.display = 'block';
    
    const threatScore = result.threat_score || 0;
    let threatLevel = 'Low';
    let threatClass = 'safe';
    
    if (threatScore >= 70) {
        threatLevel = 'High';
        threatClass = 'malicious';
    } else if (threatScore >= 40) {
        threatLevel = 'Medium';
        threatClass = 'suspicious';
    }
    
    threatResult.innerHTML = `
        <div class="result-verdict ${threatClass}">
            <i class="fas fa-shield-alt"></i>
            <span>Threat Level: ${threatLevel} (${threatScore}/100)</span>
        </div>
        
        <div class="confidence-section">
            <label>Threat Score: ${threatScore}/100</label>
            <div class="confidence-bar">
                <div class="confidence-fill ${threatClass}" style="width: ${threatScore}%"></div>
            </div>
        </div>
        
        <div class="result-details">
            <h6><i class="fas fa-info-circle"></i> Threat Intelligence Details</h6>
            <p><strong>Domain:</strong> ${result.domain}</p>
            <p><strong>URL Hash:</strong> <code>${result.url_hash}</code></p>
            
            <h6><i class="fas fa-calendar"></i> Domain Registration</h6>
            <p><strong>Creation Date:</strong> ${result.registration_info.creation_date}</p>
            <p><strong>Days Old:</strong> ${result.registration_info.days_old || 'Unknown'}</p>
            <p><strong>Registrar:</strong> ${result.registration_info.registrar}</p>
            <p><strong>Country:</strong> ${result.registration_info.country}</p>
            
            <h6><i class="fas fa-link"></i> URL Structure</h6>
            <p><strong>URL Length:</strong> ${result.structure_info.url_length} characters</p>
            <p><strong>Subdomains:</strong> ${result.structure_info.subdomain_count}</p>
            <p><strong>Has IP Address:</strong> ${result.structure_info.has_ip_address ? 'Yes' : 'No'}</p>
            <p><strong>Has Suspicious Chars:</strong> ${result.structure_info.has_suspicious_chars ? 'Yes' : 'No'}</p>
            <p><strong>Typosquatting:</strong> ${result.structure_info.has_typosquatting ? 'Yes' : 'No'}</p>
            
            <p class="text-muted mt-3">
                <small><i class="fas fa-clock"></i> Generated on ${new Date(result.timestamp).toLocaleString()}</small>
            </p>
        </div>
    `;
}

// Email Analysis
async function handleEmailAnalysis(event) {
    event.preventDefault();
    
    const emailContent = document.getElementById('email-content').value.trim();
    if (!emailContent) {
        showAlert('Please enter email content to analyze.', 'danger');
        return;
    }
    
    showLoadingModal();
    
    try {
        const response = await fetch('/email_analysis', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email_content: emailContent })
        });
        
        const result = await response.json();
        
        if (response.ok) {
            displayEmailAnalysis(result);
        } else {
            showAlert(result.error || 'Email analysis failed', 'danger');
        }
    } catch (error) {
        showAlert('Network error: ' + error.message, 'danger');
    } finally {
        hideLoadingModal();
    }
}

function displayEmailAnalysis(result) {
    const emailResult = document.getElementById('email-result');
    emailResult.style.display = 'block';
    
    const analysis = result.email_analysis;
    const threatScore = analysis.email_threat_score;
    let threatLevel = 'Low';
    let threatClass = 'safe';
    
    if (threatScore >= 70) {
        threatLevel = 'High';
        threatClass = 'malicious';
    } else if (threatScore >= 40) {
        threatLevel = 'Medium';
        threatClass = 'suspicious';
    }
    
    emailResult.innerHTML = `
        <div class="result-verdict ${threatClass}">
            <i class="fas fa-envelope"></i>
            <span>Email Threat Level: ${threatLevel} (${threatScore}/100)</span>
        </div>
        
        <div class="confidence-section">
            <label>Threat Score: ${threatScore}/100</label>
            <div class="confidence-bar">
                <div class="confidence-fill ${threatClass}" style="width: ${threatScore}%"></div>
            </div>
        </div>
        
        <div class="result-details">
            <h6><i class="fas fa-info-circle"></i> Email Analysis Details</h6>
            <p><strong>Suspicious Patterns:</strong> ${analysis.suspicious_patterns}</p>
            <p><strong>Urgency Indicators:</strong> ${analysis.urgency_indicators}</p>
            <p><strong>Action Requests:</strong> ${analysis.action_requests}</p>
            <p><strong>Likely Phishing:</strong> ${analysis.is_likely_phishing ? 'Yes' : 'No'}</p>
            
            <p class="text-muted mt-3">
                <small><i class="fas fa-clock"></i> Analyzed on ${new Date(result.timestamp).toLocaleString()}</small>
            </p>
        </div>
    `;
}

// URL Monitoring
async function handleURLMonitoring(event) {
    event.preventDefault();
    
    const url = document.getElementById('monitor-url').value.trim();
    const interval = document.getElementById('monitor-interval').value;
    
    if (!url) {
        showAlert('Please enter a URL to monitor.', 'danger');
        return;
    }
    
    showLoadingModal();
    
    try {
        const response = await fetch('/monitor_url', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                url: url, 
                interval_hours: parseInt(interval) 
            })
        });
        
        const result = await response.json();
        
        if (response.ok) {
            showAlert(result.message, 'success');
            document.getElementById('monitor-url').value = '';
            loadMonitoredURLs();
        } else {
            showAlert(result.error || 'Failed to start monitoring', 'danger');
        }
    } catch (error) {
        showAlert('Network error: ' + error.message, 'danger');
    } finally {
        hideLoadingModal();
    }
}

async function loadMonitoredURLs() {
    try {
        const response = await fetch('/monitored_urls');
        const result = await response.json();
        
        if (response.ok) {
            displayMonitoredURLs(result.monitored_urls);
        }
    } catch (error) {
        console.error('Failed to load monitored URLs:', error);
    }
}

function displayMonitoredURLs(urls) {
    const container = document.getElementById('monitored-urls-list');
    
    if (urls.length === 0) {
        container.innerHTML = '<p class="text-muted">No URLs being monitored.</p>';
        return;
    }
    
    container.innerHTML = urls.map(url => `
        <div class="d-flex justify-content-between align-items-center mb-2 p-2 border rounded">
            <span class="text-truncate" style="max-width: 300px;">${url}</span>
            <button class="btn btn-sm btn-outline-danger" onclick="stopMonitoring('${url}')">
                <i class="fas fa-stop"></i> Stop
            </button>
        </div>
    `).join('');
}

async function stopMonitoring(url) {
    try {
        const response = await fetch('/stop_monitoring', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url: url })
        });
        
        const result = await response.json();
        
        if (response.ok) {
            showAlert(result.message, 'success');
            loadMonitoredURLs();
        } else {
            showAlert(result.error || 'Failed to stop monitoring', 'danger');
        }
    } catch (error) {
        showAlert('Network error: ' + error.message, 'danger');
    }
}

// Dashboard
async function loadDashboard() {
    try {
        const response = await fetch('/threat_dashboard');
        const result = await response.json();
        
        if (response.ok) {
            displayDashboard(result.dashboard);
        }
    } catch (error) {
        console.error('Failed to load dashboard:', error);
    }
}

function displayDashboard(dashboard) {
    const stats = dashboard.statistics;
    
    // Update statistics cards
    document.getElementById('total-analyzed').textContent = stats.total_analyzed || 0;
    document.getElementById('safe-count').textContent = stats.safe_count || 0;
    document.getElementById('suspicious-count').textContent = stats.suspicious_count || 0;
    document.getElementById('malicious-count').textContent = stats.malicious_count || 0;
    
    // Update system status
    const systemStatus = document.getElementById('system-status');
    systemStatus.innerHTML = `
        <p><i class="fas fa-check-circle text-success"></i> System Operational</p>
        <p><i class="fas fa-robot text-info"></i> AI Analysis Active</p>
        <p><i class="fas fa-database text-primary"></i> Threat Database Updated</p>
        <p><i class="fas fa-eye text-warning"></i> ${dashboard.total_monitored} URLs Monitored</p>
    `;
}

// Add some sample URLs for testing
function addSampleUrls() {
    const sampleUrls = [
        'https://www.google.com',
        'https://www.github.com',
        'https://example.com',
        'https://bit.ly/3abc123',
        'https://suspicious-site.com'
    ];
    
    document.getElementById('batch-urls').value = sampleUrls.join('\n');
}
