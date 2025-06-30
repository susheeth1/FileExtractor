# Code Tokenizer - Flask Application

A Flask web application that extracts, tokenizes, and displays code from ZIP files or GitHub repositories. The application analyzes different programming languages and provides tokenized text output.

## Features

- Upload ZIP files containing code projects
- Clone and process GitHub repositories
- Support for multiple programming languages (Python, Java, JavaScript, HTML, CSS, etc.)
- Tokenization and preprocessing of code files
- Download tokenized content in TXT format
- Web-based interface with drag-and-drop support

## Installation and Setup

### Prerequisites

- Python 3.11 or higher
- Git (for GitHub repository cloning)

### Local Installation

1. **Clone or download this repository**
   ```bash
   git clone <repository-url>
   cd code-tokenizer
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables** (optional)
   ```bash
   # For production, set these environment variables:
   export SESSION_SECRET="your-secret-key-here"
   export DATABASE_URL="sqlite:///tokenizer.db"  # or PostgreSQL URL
   ```

5. **Run the application**
   ```bash
   python main.py
   ```

6. **Access the application**
   Open your web browser and go to: `http://localhost:5000`

### Dependencies

The application requires these Python packages:
- Flask
- Flask-SQLAlchemy
- Werkzeug
- GitPython (for GitHub repository cloning)
- Requests
- Gunicorn (for production deployment)

### Directory Structure

```
code-tokenizer/
├── app.py              # Main Flask application
├── main.py             # Application entry point
├── file_processor.py   # File processing logic
├── tokenizers.py       # Code tokenization modules
├── models.py           # Database models
├── templates/          # HTML templates
│   ├── index.html      # Upload interface
│   └── results.html    # Results display
├── static/             # CSS, JS, and assets
│   ├── css/
│   └── js/
├── uploads/            # Temporary file uploads
├── temp/               # Temporary processing files
└── requirements.txt    # Python dependencies
```

## Usage

1. **Upload a ZIP file**: Drag and drop or browse for a ZIP file containing your code project
2. **Or enter a GitHub URL**: Provide a GitHub repository URL to clone and process
3. **View results**: See tokenized content organized by programming language
4. **Download**: Download individual language tokens or all tokenized content as TXT files

## Supported File Types

- **Programming Languages**: Python (.py), Java (.java), JavaScript (.js, .jsx), TypeScript (.ts, .tsx), HTML (.html, .htm), CSS (.css, .scss, .sass, .less), C/C++ (.c, .cpp, .h, .hpp), C# (.cs), PHP (.php), Ruby (.rb), Go (.go), Rust (.rs), and many more
- **Configuration Files**: JSON, XML, YAML, TOML, INI
- **Documentation**: Markdown, text files
- **Images**: JPG, PNG, GIF, SVG, etc.

## Configuration

### Environment Variables

- `SESSION_SECRET`: Flask session secret key (required for production)
- `DATABASE_URL`: Database connection string (defaults to SQLite)

### File Upload Settings

- Maximum file size: 100MB
- Supported formats: ZIP files for upload
- GitHub repositories: Public repositories accessible via HTTPS

## Troubleshooting

### Common Issues

1. **Permission errors**: Ensure the application has write access to `uploads/` and `temp/` directories
2. **Git not found**: Install Git if you plan to use GitHub repository processing
3. **Large files**: Files over 100MB will be rejected - consider splitting large projects

### Error Logs

The application uses Python logging. Check console output for detailed error messages.

## Development

### Running in Development Mode

```bash
# Enable debug mode
export FLASK_ENV=development
python main.py
```

### Database Setup

The application automatically creates necessary database tables on first run using SQLite by default.

## Security Considerations

- Set a strong `SESSION_SECRET` in production
- Consider file upload size limits for your use case
- Validate and sanitize uploaded content
- Use HTTPS in production environments

## License

This project is available under the MIT License.