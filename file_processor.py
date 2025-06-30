import os
import zipfile
import tempfile
import shutil
import logging
from typing import Dict, List, Any
from urllib.parse import urlparse
import mimetypes
import subprocess
from tokenizers import get_tokenizer

logger = logging.getLogger(__name__)

class FileProcessor:
    """Process zip files and GitHub repositories"""
    
    def __init__(self):
        self.supported_code_extensions = {
            '.py': 'Python',
            '.java': 'Java',
            '.js': 'JavaScript',
            '.jsx': 'React JSX',
            '.ts': 'TypeScript',
            '.tsx': 'React TSX',
            '.html': 'HTML',
            '.htm': 'HTML',
            '.css': 'CSS',
            '.scss': 'SCSS',
            '.sass': 'SASS',
            '.less': 'LESS',
            '.c': 'C',
            '.cpp': 'C++',
            '.cc': 'C++',
            '.cxx': 'C++',
            '.h': 'C Header',
            '.hpp': 'C++ Header',
            '.cs': 'C#',
            '.php': 'PHP',
            '.rb': 'Ruby',
            '.go': 'Go',
            '.rs': 'Rust',
            '.kt': 'Kotlin',
            '.kts': 'Kotlin Script',
            '.swift': 'Swift',
            '.scala': 'Scala',
            '.r': 'R',
            '.m': 'Objective-C',
            '.mm': 'Objective-C++',
            '.pl': 'Perl',
            '.pm': 'Perl Module',
            '.sh': 'Shell',
            '.bash': 'Bash',
            '.zsh': 'Zsh',
            '.fish': 'Fish',
            '.bat': 'Batch',
            '.cmd': 'Command',
            '.ps1': 'PowerShell',
            '.psm1': 'PowerShell Module',
            '.vue': 'Vue',
            '.svelte': 'Svelte',
            '.dart': 'Dart',
            '.lua': 'Lua',
            '.sql': 'SQL',
            '.xml': 'XML',
            '.xsl': 'XSL',
            '.xslt': 'XSLT',
        }
        
        self.image_extensions = {
            '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp', '.ico'
        }
        
        self.document_extensions = {
            '.txt', '.md', '.rst', '.pdf', '.doc', '.docx', '.rtf'
        }
        
        self.config_extensions = {
            '.json', '.xml', '.yaml', '.yml', '.toml', '.ini', '.conf', '.cfg'
        }
    
    def process_zip_file(self, zip_path: str) -> Dict[str, Any]:
        """Process a ZIP file and tokenize its contents"""
        try:
            temp_dir = tempfile.mkdtemp()
            
            try:
                # Extract ZIP file
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(temp_dir)
                
                # Process extracted files
                result = self._process_directory(temp_dir)
                
                return {
                    'success': True,
                    'tokenized_files': result
                }
                
            finally:
                # Clean up temporary directory
                shutil.rmtree(temp_dir, ignore_errors=True)
                
        except Exception as e:
            logger.error(f"Error processing ZIP file: {str(e)}")
            return {
                'success': False,
                'error': f"Error processing ZIP file: {str(e)}"
            }
    
    def process_github_repo(self, github_url: str) -> Dict[str, Any]:
        """Clone and process a GitHub repository"""
        try:
            # Validate GitHub URL
            if not self._is_valid_github_url(github_url):
                return {
                    'success': False,
                    'error': "Invalid GitHub URL format"
                }
            
            temp_dir = tempfile.mkdtemp()
            
            try:
                # Clone repository
                result = subprocess.run([
                    'git', 'clone', github_url, temp_dir
                ], capture_output=True, text=True, timeout=300)
                
                if result.returncode != 0:
                    return {
                        'success': False,
                        'error': f"Failed to clone repository: {result.stderr}"
                    }
                
                # Process cloned repository
                processed_result = self._process_directory(temp_dir)
                
                return {
                    'success': True,
                    'tokenized_files': processed_result
                }
                
            finally:
                # Clean up temporary directory
                shutil.rmtree(temp_dir, ignore_errors=True)
                
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': "Repository cloning timed out (5 minutes limit)"
            }
        except Exception as e:
            logger.error(f"Error processing GitHub repository: {str(e)}")
            return {
                'success': False,
                'error': f"Error processing GitHub repository: {str(e)}"
            }
    
    def _is_valid_github_url(self, url: str) -> bool:
        """Validate GitHub URL format"""
        try:
            parsed = urlparse(url)
            return (
                parsed.scheme in ['http', 'https'] and
                'github.com' in parsed.netloc and
                len(parsed.path.strip('/').split('/')) >= 2
            )
        except:
            return False
    
    def _process_directory(self, directory: str) -> Dict[str, List[Dict]]:
        """Process all files in a directory and organize by type"""
        result = {
            'code_files': {},
            'image_files': [],
            'document_files': [],
            'config_files': [],
            'other_files': []
        }
        
        for root, dirs, files in os.walk(directory):
            # Skip hidden directories and common build/cache directories
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', 'build', 'dist', 'target']]
            
            for file in files:
                if file.startswith('.'):
                    continue
                    
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, directory)
                file_ext = os.path.splitext(file)[1].lower()
                
                try:
                    file_info = {
                        'name': file,
                        'path': relative_path,
                        'size': os.path.getsize(file_path),
                        'extension': file_ext
                    }
                    
                    # Process based on file type
                    if file_ext in self.supported_code_extensions:
                        self._process_code_file(file_path, file_info, result)
                    elif file_ext in self.image_extensions:
                        result['image_files'].append(file_info)
                    elif file_ext in self.document_extensions:
                        result['document_files'].append(file_info)
                    elif file_ext in self.config_extensions:
                        self._process_config_file(file_path, file_info, result)
                    else:
                        result['other_files'].append(file_info)
                        
                except Exception as e:
                    logger.error(f"Error processing file {file_path}: {str(e)}")
                    continue
        
        return result
    
    def _process_code_file(self, file_path: str, file_info: Dict, result: Dict):
        """Process and tokenize a code file"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            file_ext = file_info['extension']
            language = self.supported_code_extensions[file_ext]
            
            # Get appropriate tokenizer
            tokenizer = get_tokenizer(file_ext)
            tokenization_result = tokenizer.tokenize(content, file_info['name'])
            
            if tokenization_result['success']:
                # Create tokenized text preview (just token names)
                token_preview = ' '.join([token['type'] for token in tokenization_result['tokens'][:200]])
                
                file_info.update({
                    'language': language,
                    'tokens': tokenization_result['tokens'],
                    'token_types': tokenization_result['token_types'],
                    'total_tokens': tokenization_result['total_tokens'],
                    'lines': len(content.splitlines()),
                    'token_preview': token_preview,
                    'full_token_string': ' '.join([token['type'] for token in tokenization_result['tokens']])
                })
                
                if language not in result['code_files']:
                    result['code_files'][language] = []
                result['code_files'][language].append(file_info)
            else:
                logger.error(f"Tokenization failed for {file_path}: {tokenization_result.get('error', 'Unknown error')}")
                
        except Exception as e:
            logger.error(f"Error processing code file {file_path}: {str(e)}")
    
    def _process_config_file(self, file_path: str, file_info: Dict, result: Dict):
        """Process configuration files"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            file_info.update({
                'content': content[:500] + '...' if len(content) > 500 else content,  # Preview
                'lines': len(content.splitlines())
            })
            
            result['config_files'].append(file_info)
            
        except Exception as e:
            logger.error(f"Error processing config file {file_path}: {str(e)}")
