import os
import logging
import json
import uuid
from datetime import datetime
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for, send_file
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.utils import secure_filename
import zipfile
import tempfile
import shutil
from file_processor import FileProcessor

logging.basicConfig(level=logging.DEBUG)

# create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# File upload configuration
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['TEMP_FOLDER'] = 'temp'
app.config['RESULTS_FOLDER'] = 'results'

# Ensure directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['TEMP_FOLDER'], exist_ok=True)
os.makedirs(app.config['RESULTS_FOLDER'], exist_ok=True)

# Initialize file processor
file_processor = FileProcessor()

# In-memory storage for current session results
session_results = {}

def save_results_to_file(session_id, results):
    """Save processing results to a JSON file"""
    results_file = os.path.join(app.config['RESULTS_FOLDER'], f"{session_id}.json")
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)

def load_results_from_file(session_id):
    """Load processing results from a JSON file"""
    results_file = os.path.join(app.config['RESULTS_FOLDER'], f"{session_id}.json")
    if os.path.exists(results_file):
        with open(results_file, 'r') as f:
            return json.load(f)
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        # Generate unique session ID
        session_id = str(uuid.uuid4())
        
        if 'file' in request.files and request.files['file'].filename:
            # Handle file upload
            file = request.files['file']
            if not file.filename or file.filename == '':
                flash('No file selected', 'error')
                return redirect(url_for('index'))
            
            if file and file.filename and file.filename.lower().endswith('.zip'):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{session_id}_{filename}")
                file.save(file_path)
                
                # Process the ZIP file
                results = file_processor.process_zip_file(file_path)
                results['session_id'] = session_id
                results['source_type'] = 'zip'
                results['source_name'] = filename
                results['processed_at'] = datetime.now().isoformat()
                
                # Save results
                session_results[session_id] = results
                save_results_to_file(session_id, results)
                
                # Clean up uploaded file
                os.remove(file_path)
                
                return redirect(url_for('show_results', session_id=session_id))
            else:
                flash('Please upload a ZIP file', 'error')
                return redirect(url_for('index'))
                
        elif 'github_url' in request.form and request.form['github_url'].strip():
            # Handle GitHub URL
            github_url = request.form['github_url'].strip()
            
            # Process the GitHub repository
            results = file_processor.process_github_repo(github_url)
            results['session_id'] = session_id
            results['source_type'] = 'github'
            results['source_name'] = github_url
            results['processed_at'] = datetime.now().isoformat()
            
            # Save results
            session_results[session_id] = results
            save_results_to_file(session_id, results)
            
            return redirect(url_for('show_results', session_id=session_id))
        else:
            flash('Please provide either a ZIP file or GitHub URL', 'error')
            return redirect(url_for('index'))
            
    except Exception as e:
        logging.error(f"Upload error: {str(e)}")
        flash(f'Error processing file: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/results/<session_id>')
def show_results(session_id):
    """Display processing results"""
    # Try to get results from memory first, then from file
    results = session_results.get(session_id)
    if not results:
        results = load_results_from_file(session_id)
    
    if not results:
        flash('Results not found or expired', 'error')
        return redirect(url_for('index'))
    
    return render_template('results.html', results=results)

@app.route('/download/<file_type>/<session_id>')
def download_tokens(file_type, session_id):
    """Download tokenized content for a specific file type"""
    # Get results
    results = session_results.get(session_id)
    if not results:
        results = load_results_from_file(session_id)
    
    if not results or file_type not in results:
        flash('Results not found', 'error')
        return redirect(url_for('index'))
    
    # Create temporary file with tokenized content
    temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False)
    
    try:
        # Write header
        temp_file.write(f"# Tokenized {file_type.upper()} Content\n")
        temp_file.write(f"# Generated: {datetime.now().isoformat()}\n")
        temp_file.write(f"# Source: {results.get('source_name', 'Unknown')}\n\n")
        
        # Write tokenized content for each file
        for file_info in results[file_type]:
            if 'full_token_string' in file_info:
                temp_file.write(f"# File: {file_info['name']}\n")
                temp_file.write(f"# Tokens: {file_info.get('total_tokens', 0)}\n")
                temp_file.write(file_info['full_token_string'])
                temp_file.write("\n\n" + "="*50 + "\n\n")
        
        temp_file.close()
        
        # Return file for download
        return send_file(
            temp_file.name,
            as_attachment=True,
            download_name=f"{file_type}_tokens.txt",
            mimetype='text/plain'
        )
        
    except Exception as e:
        logging.error(f"Download error: {str(e)}")
        if os.path.exists(temp_file.name):
            os.unlink(temp_file.name)
        flash('Error creating download file', 'error')
        return redirect(url_for('show_results', session_id=session_id))

@app.route('/download_all/<session_id>')
def download_all_tokens(session_id):
    """Download all tokenized content as a single file"""
    # Get results
    results = session_results.get(session_id)
    if not results:
        results = load_results_from_file(session_id)
    
    if not results:
        flash('Results not found', 'error')
        return redirect(url_for('index'))
    
    # Create temporary file with all tokenized content
    temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False)
    
    try:
        # Write header
        temp_file.write(f"# All Tokenized Content\n")
        temp_file.write(f"# Generated: {datetime.now().isoformat()}\n")
        temp_file.write(f"# Source: {results.get('source_name', 'Unknown')}\n\n")
        
        # Write content for each file type
        for file_type in ['python', 'javascript', 'java', 'html', 'css', 'other']:
            if file_type in results and results[file_type]:
                temp_file.write(f"\n{'='*60}\n")
                temp_file.write(f"# {file_type.upper()} FILES\n")
                temp_file.write(f"{'='*60}\n\n")
                
                for file_info in results[file_type]:
                    if 'full_token_string' in file_info:
                        temp_file.write(f"## File: {file_info['name']}\n")
                        temp_file.write(f"## Tokens: {file_info.get('total_tokens', 0)}\n")
                        temp_file.write(file_info['full_token_string'])
                        temp_file.write("\n\n" + "-"*40 + "\n\n")
        
        temp_file.close()
        
        # Return file for download
        return send_file(
            temp_file.name,
            as_attachment=True,
            download_name=f"all_tokens.txt",
            mimetype='text/plain'
        )
        
    except Exception as e:
        logging.error(f"Download all error: {str(e)}")
        if os.path.exists(temp_file.name):
            os.unlink(temp_file.name)
        flash('Error creating download file', 'error')
        return redirect(url_for('show_results', session_id=session_id))

@app.errorhandler(413)
def too_large(e):
    flash('File too large. Maximum size is 100MB.', 'error')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)