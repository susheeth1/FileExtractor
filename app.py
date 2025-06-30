import os
import logging
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for, send_file
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.utils import secure_filename
import zipfile
import tempfile
import shutil
from file_processor import FileProcessor

logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///tokenizer.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# File upload configuration
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['TEMP_FOLDER'] = 'temp'

# Ensure directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['TEMP_FOLDER'], exist_ok=True)

# initialize the app with the extension
db.init_app(app)

# Initialize file processor
file_processor = FileProcessor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files and 'github_url' not in request.form:
            flash('No file or GitHub URL provided', 'error')
            return redirect(url_for('index'))
        
        github_url = request.form.get('github_url', '').strip()
        
        if github_url:
            # Process GitHub repository
            result = file_processor.process_github_repo(github_url)
        else:
            # Process uploaded file
            file = request.files['file']
            if file.filename == '':
                flash('No file selected', 'error')
                return redirect(url_for('index'))
            
            if not file.filename or not str(file.filename).lower().endswith('.zip'):
                flash('Only ZIP files are supported', 'error')
                return redirect(url_for('index'))
            
            # Save uploaded file
            filename = secure_filename(str(file.filename))
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Process the file
            result = file_processor.process_zip_file(file_path)
            
            # Clean up uploaded file
            os.remove(file_path)
        
        if result['success']:
            # Store tokenized data in session for download functionality
            from flask import session
            session['tokenized_files'] = result['tokenized_files']
            
            return render_template('results.html', 
                                 tokenized_files=result['tokenized_files'],
                                 source=github_url if github_url else 'Uploaded ZIP file')
        else:
            flash(result['error'], 'error')
            return redirect(url_for('index'))
            
    except Exception as e:
        app.logger.error(f"Error processing upload: {str(e)}")
        flash(f'Error processing file: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/download/<file_type>')
def download_tokens(file_type):
    """Download tokenized content for a specific file type"""
    try:
        from flask import session
        
        # Get tokenized data from session
        tokenized_files = session.get('tokenized_files', {})
        code_files = tokenized_files.get('code_files', {})
        
        if file_type not in code_files:
            flash(f'No tokenized data found for {file_type}', 'error')
            return redirect(url_for('index'))
        
        # Create tokenized text content
        content_lines = []
        content_lines.append(f"=== TOKENIZED {file_type.upper()} FILES ===\n")
        
        for file_data in code_files[file_type]:
            content_lines.append(f"FILE: {file_data['name']}")
            content_lines.append(f"LINES: {file_data['lines']}")
            content_lines.append(f"TOTAL_TOKENS: {file_data['total_tokens']}")
            content_lines.append("TOKEN_TYPES: " + " ".join([f"{k}:{v}" for k, v in file_data['token_types'].items()]))
            content_lines.append("TOKENS: " + file_data['full_token_string'])
            content_lines.append("-" * 80)
            content_lines.append("")
        
        # Write to temporary file
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8')
        temp_file.write('\n'.join(content_lines))
        temp_file.close()
        
        return send_file(temp_file.name, 
                        as_attachment=True, 
                        download_name=f'{file_type}_tokens.txt',
                        mimetype='text/plain')
                        
    except Exception as e:
        app.logger.error(f"Error downloading tokens: {str(e)}")
        flash(f'Error downloading tokens: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/download_all')
def download_all_tokens():
    """Download all tokenized content as a single file"""
    try:
        from flask import session
        
        # Get tokenized data from session
        tokenized_files = session.get('tokenized_files', {})
        code_files = tokenized_files.get('code_files', {})
        
        if not code_files:
            flash('No tokenized data found', 'error')
            return redirect(url_for('index'))
        
        # Create comprehensive tokenized text content
        content_lines = []
        content_lines.append("=== ALL TOKENIZED FILES ===\n")
        
        for language, files in code_files.items():
            content_lines.append(f"\n=== {language.upper()} FILES ===")
            content_lines.append(f"Total Files: {len(files)}")
            content_lines.append("")
            
            for file_data in files:
                content_lines.append(f"FILE: {file_data['name']}")
                content_lines.append(f"LINES: {file_data['lines']}")
                content_lines.append(f"TOTAL_TOKENS: {file_data['total_tokens']}")
                content_lines.append("TOKEN_TYPES: " + " ".join([f"{k}:{v}" for k, v in file_data['token_types'].items()]))
                content_lines.append("TOKENS: " + file_data['full_token_string'])
                content_lines.append("-" * 80)
                content_lines.append("")
        
        # Write to temporary file
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8')
        temp_file.write('\n'.join(content_lines))
        temp_file.close()
        
        return send_file(temp_file.name, 
                        as_attachment=True, 
                        download_name='all_tokens.txt',
                        mimetype='text/plain')
                        
    except Exception as e:
        app.logger.error(f"Error downloading all tokens: {str(e)}")
        flash(f'Error downloading all tokens: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.errorhandler(413)
def too_large(e):
    flash('File too large. Maximum size is 100MB.', 'error')
    return redirect(url_for('index'))

with app.app_context():
    import models
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
