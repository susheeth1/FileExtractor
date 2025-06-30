# Code Tokenizer - Flask Application

## Overview

This is a Flask-based web application that extracts and tokenizes code from ZIP files or GitHub repositories. The application analyzes different programming languages, counts tokens, and provides detailed tokenization results through a web interface.

## System Architecture

### Frontend Architecture
- **Technology**: HTML templates with Bootstrap 5 (dark theme)
- **JavaScript**: Vanilla JS for file upload handling, drag-and-drop functionality
- **CSS**: Custom styling with CSS variables for theming
- **UI Components**: Responsive cards, forms, and result displays

### Backend Architecture
- **Framework**: Flask with SQLAlchemy ORM
- **Database**: SQLite (development) with PostgreSQL support via environment configuration
- **File Processing**: Custom FileProcessor class for handling ZIP files and code extraction
- **Tokenization**: Language-specific tokenizers (Python tokenizer implemented)

### Data Storage
- **Primary Database**: SQLite/PostgreSQL via SQLAlchemy
- **File Storage**: Local filesystem with configurable upload and temp directories
- **Session Management**: Flask sessions with configurable secret key

## Key Components

### 1. Application Core (`app.py`)
- Flask application setup with ProxyFix middleware
- Database configuration with connection pooling
- File upload configuration (100MB max size)
- Route definitions and error handling

### 2. File Processing (`file_processor.py`)
- Supports multiple programming languages (.py, .js, .java, .cpp, etc.)
- Handles ZIP file extraction and GitHub repository processing
- Image and document file recognition
- Extensible architecture for adding new file types

### 3. Database Models (`models.py`)
- `ProcessedFile`: Stores metadata about processed files
- `TokenizedContent`: Stores tokenization results with foreign key relationship
- Timestamps and file type tracking

### 4. Tokenization Engine (`tokenizers.py`)
- `CodeTokenizer`: Base class for language-specific tokenizers
- `PythonTokenizer`: Python-specific tokenizer using built-in tokenize module
- Structured token output with type counting and position tracking

### 5. Web Interface
- **Templates**: Jinja2 templates with Bootstrap styling
- **Static Assets**: Custom CSS and JavaScript for enhanced UX
- **File Upload**: Drag-and-drop interface with progress indicators

## Data Flow

1. **File Input**: User uploads ZIP file or provides GitHub URL
2. **Extraction**: FileProcessor extracts and categorizes files
3. **Tokenization**: Language-specific tokenizers process code files
4. **Storage**: Results stored in database with file metadata
5. **Display**: Tokenization results presented through web interface

## External Dependencies

### Python Packages
- Flask: Web framework
- Flask-SQLAlchemy: Database ORM
- Werkzeug: WSGI utilities and file handling
- tokenizers: Code tokenization (custom implementation)

### Frontend Libraries
- Bootstrap 5: UI framework with dark theme
- Font Awesome 6: Icons
- Prism.js: Code syntax highlighting

### System Dependencies
- Git: For GitHub repository cloning (implied)
- File system access for temporary file processing

## Deployment Strategy

### Environment Configuration
- `DATABASE_URL`: Database connection string (defaults to SQLite)
- `SESSION_SECRET`: Flask session secret key
- Configurable upload and temp directories

### File System Requirements
- Write access to uploads and temp directories
- Sufficient disk space for file processing
- Cleanup mechanisms for temporary files

### Database Setup
- SQLAlchemy migrations support
- Connection pooling with health checks
- Support for both SQLite (dev) and PostgreSQL (production)

## Local Installation

To run this application locally:

1. **Download the project files** from this Replit or copy all files to your local machine

2. **Install Python 3.11+** on your system

3. **Set up the environment**:
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate it (Windows)
   venv\Scripts\activate
   
   # Activate it (Mac/Linux)  
   source venv/bin/activate
   
   # Install minimal dependencies (no database required)
   pip install Flask Werkzeug GitPython requests
   ```

4. **Run the application**:
   ```bash
   python main.py
   ```

5. **Access at**: http://localhost:5000

### Even Easier Setup
Run `python setup.py` for fully automated installation - it only installs 4 simple packages now.

### Requirements
- Python 3.11+
- Git (for GitHub repository processing)
- Web browser
- 100MB+ free disk space for file processing

### No Database Needed
The application now uses simple file storage and memory - no SQL databases required!

## Deployment
- Replit deployment: Use the Deploy button in Replit interface
- Local development: Follow installation steps above
- Production: Set SESSION_SECRET environment variable

## Changelog
- June 30, 2025: Initial setup with ZIP and GitHub processing
- June 30, 2025: Updated tokenization to output actual text content (not type labels)
- June 30, 2025: Added local installation documentation and setup script

## User Preferences

Preferred communication style: Simple, everyday language.
User requested tokenized output as actual text content without token type labels.