import tokenize
import io
import re
import logging
from typing import Dict, List, Any

logger = logging.getLogger(__name__)

class CodeTokenizer:
    """Base class for code tokenizers"""
    
    def tokenize(self, content: str, filename: str) -> Dict[str, Any]:
        """Tokenize content and return structured data"""
        raise NotImplementedError

class PythonTokenizer(CodeTokenizer):
    """Python code tokenizer using built-in tokenize module"""
    
    def tokenize(self, content: str, filename: str) -> Dict[str, Any]:
        try:
            tokens = []
            token_types = {}
            
            # Create a StringIO object from the content
            content_io = io.StringIO(content)
            
            # Tokenize the Python code
            for tok in tokenize.generate_tokens(content_io.readline):
                token_info = {
                    'type': tokenize.tok_name[tok.type],
                    'string': tok.string,
                    'start': tok.start,
                    'end': tok.end,
                    'line': tok.line
                }
                tokens.append(token_info)
                
                # Count token types
                token_type = tokenize.tok_name[tok.type]
                token_types[token_type] = token_types.get(token_type, 0) + 1
            
            return {
                'success': True,
                'tokens': tokens,
                'token_types': token_types,
                'total_tokens': len(tokens),
                'filename': filename
            }
            
        except Exception as e:
            logger.error(f"Error tokenizing Python file {filename}: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'filename': filename
            }

class JavaTokenizer(CodeTokenizer):
    """Java code tokenizer using regex patterns"""
    
    def __init__(self):
        # Java token patterns
        self.token_patterns = [
            ('COMMENT', r'//.*?$|/\*.*?\*/'),
            ('STRING', r'"([^"\\]|\\.)*"'),
            ('CHAR', r"'([^'\\]|\\.)*'"),
            ('NUMBER', r'\b\d+\.?\d*\b'),
            ('KEYWORD', r'\b(abstract|assert|boolean|break|byte|case|catch|char|class|const|continue|default|do|double|else|enum|extends|final|finally|float|for|goto|if|implements|import|instanceof|int|interface|long|native|new|null|package|private|protected|public|return|short|static|strictfp|super|switch|synchronized|this|throw|throws|transient|try|void|volatile|while)\b'),
            ('IDENTIFIER', r'\b[a-zA-Z_]\w*\b'),
            ('OPERATOR', r'[+\-*/%=<>!&|^~?:]+'),
            ('DELIMITER', r'[(){}\[\];,.@]'),
            ('WHITESPACE', r'\s+'),
        ]
        
        self.compiled_patterns = [(name, re.compile(pattern, re.MULTILINE | re.DOTALL)) 
                                 for name, pattern in self.token_patterns]
    
    def tokenize(self, content: str, filename: str) -> Dict[str, Any]:
        try:
            tokens = []
            token_types = {}
            pos = 0
            line_num = 1
            
            while pos < len(content):
                matched = False
                
                for token_type, pattern in self.compiled_patterns:
                    match = pattern.match(content, pos)
                    if match:
                        token_string = match.group(0)
                        
                        if token_type != 'WHITESPACE':  # Skip whitespace tokens
                            token_info = {
                                'type': token_type,
                                'string': token_string,
                                'line': line_num,
                                'position': pos
                            }
                            tokens.append(token_info)
                            token_types[token_type] = token_types.get(token_type, 0) + 1
                        
                        # Update line number
                        line_num += token_string.count('\n')
                        pos = match.end()
                        matched = True
                        break
                
                if not matched:
                    # Skip unrecognized character
                    pos += 1
            
            return {
                'success': True,
                'tokens': tokens,
                'token_types': token_types,
                'total_tokens': len(tokens),
                'filename': filename
            }
            
        except Exception as e:
            logger.error(f"Error tokenizing Java file {filename}: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'filename': filename
            }

class JavaScriptTokenizer(CodeTokenizer):
    """JavaScript code tokenizer using regex patterns"""
    
    def __init__(self):
        # JavaScript token patterns
        self.token_patterns = [
            ('COMMENT', r'//.*?$|/\*.*?\*/'),
            ('REGEX', r'/(?:[^/\\\n]|\\.)+/[gimuy]*'),
            ('STRING', r'"([^"\\]|\\.)*"|\'([^\'\\]|\\.)*\'|`([^`\\]|\\.)*`'),
            ('NUMBER', r'\b\d+\.?\d*([eE][+-]?\d+)?\b'),
            ('KEYWORD', r'\b(async|await|break|case|catch|class|const|continue|debugger|default|delete|do|else|export|extends|finally|for|function|if|import|in|instanceof|let|new|return|super|switch|this|throw|try|typeof|var|void|while|with|yield)\b'),
            ('BOOLEAN', r'\b(true|false)\b'),
            ('NULL', r'\bnull\b'),
            ('UNDEFINED', r'\bundefined\b'),
            ('IDENTIFIER', r'\b[a-zA-Z_$]\w*\b'),
            ('OPERATOR', r'[+\-*/%=<>!&|^~?:]+|===|!==|==|!=|<=|>=|&&|\|\||<<|>>|>>>|\+\+|--|\+=|-=|\*=|/=|%=|&=|\|=|\^=|<<=|>>=|>>>='),
            ('DELIMITER', r'[(){}\[\];,.@]'),
            ('WHITESPACE', r'\s+'),
        ]
        
        self.compiled_patterns = [(name, re.compile(pattern, re.MULTILINE | re.DOTALL)) 
                                 for name, pattern in self.token_patterns]
    
    def tokenize(self, content: str, filename: str) -> Dict[str, Any]:
        try:
            tokens = []
            token_types = {}
            pos = 0
            line_num = 1
            
            while pos < len(content):
                matched = False
                
                for token_type, pattern in self.compiled_patterns:
                    match = pattern.match(content, pos)
                    if match:
                        token_string = match.group(0)
                        
                        if token_type != 'WHITESPACE':  # Skip whitespace tokens
                            token_info = {
                                'type': token_type,
                                'string': token_string,
                                'line': line_num,
                                'position': pos
                            }
                            tokens.append(token_info)
                            token_types[token_type] = token_types.get(token_type, 0) + 1
                        
                        # Update line number
                        line_num += token_string.count('\n')
                        pos = match.end()
                        matched = True
                        break
                
                if not matched:
                    # Skip unrecognized character
                    pos += 1
            
            return {
                'success': True,
                'tokens': tokens,
                'token_types': token_types,
                'total_tokens': len(tokens),
                'filename': filename
            }
            
        except Exception as e:
            logger.error(f"Error tokenizing JavaScript file {filename}: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'filename': filename
            }

class HTMLTokenizer(CodeTokenizer):
    """HTML tokenizer using regex patterns"""
    
    def __init__(self):
        self.token_patterns = [
            ('COMMENT', r'<!--.*?-->'),
            ('DOCTYPE', r'<!DOCTYPE[^>]*>'),
            ('TAG_OPEN', r'<[a-zA-Z][^>]*>'),
            ('TAG_CLOSE', r'</[a-zA-Z][^>]*>'),
            ('TAG_SELF_CLOSE', r'<[a-zA-Z][^>]*/\s*>'),
            ('ATTRIBUTE', r'\b[a-zA-Z-]+\s*=\s*["\'][^"\']*["\']'),
            ('TEXT', r'>[^<]+<'),
            ('WHITESPACE', r'\s+'),
        ]
        
        self.compiled_patterns = [(name, re.compile(pattern, re.MULTILINE | re.DOTALL)) 
                                 for name, pattern in self.token_patterns]
    
    def tokenize(self, content: str, filename: str) -> Dict[str, Any]:
        try:
            tokens = []
            token_types = {}
            pos = 0
            line_num = 1
            
            while pos < len(content):
                matched = False
                
                for token_type, pattern in self.compiled_patterns:
                    match = pattern.match(content, pos)
                    if match:
                        token_string = match.group(0)
                        
                        if token_type != 'WHITESPACE':
                            token_info = {
                                'type': token_type,
                                'line': line_num,
                                'position': pos
                            }
                            tokens.append(token_info)
                            token_types[token_type] = token_types.get(token_type, 0) + 1
                        
                        line_num += token_string.count('\n')
                        pos = match.end()
                        matched = True
                        break
                
                if not matched:
                    pos += 1
            
            return {
                'success': True,
                'tokens': tokens,
                'token_types': token_types,
                'total_tokens': len(tokens),
                'filename': filename
            }
            
        except Exception as e:
            logger.error(f"Error tokenizing HTML file {filename}: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'filename': filename
            }

class CSSTokenizer(CodeTokenizer):
    """CSS tokenizer using regex patterns"""
    
    def __init__(self):
        self.token_patterns = [
            ('COMMENT', r'/\*.*?\*/'),
            ('SELECTOR', r'[a-zA-Z0-9_.-]+(?:\s*,\s*[a-zA-Z0-9_.-]+)*\s*(?=\{)'),
            ('PROPERTY', r'[a-zA-Z-]+\s*:'),
            ('VALUE', r':\s*[^;{}]+'),
            ('BRACE_OPEN', r'\{'),
            ('BRACE_CLOSE', r'\}'),
            ('SEMICOLON', r';'),
            ('AT_RULE', r'@[a-zA-Z-]+'),
            ('STRING', r'"[^"]*"|\'[^\']*\''),
            ('NUMBER', r'\b\d+(?:\.\d+)?(?:px|em|rem|%|vh|vw|pt|pc|in|cm|mm)?\b'),
            ('COLOR', r'#[0-9A-Fa-f]{3,8}'),
            ('WHITESPACE', r'\s+'),
        ]
        
        self.compiled_patterns = [(name, re.compile(pattern, re.MULTILINE | re.DOTALL)) 
                                 for name, pattern in self.token_patterns]
    
    def tokenize(self, content: str, filename: str) -> Dict[str, Any]:
        try:
            tokens = []
            token_types = {}
            pos = 0
            line_num = 1
            
            while pos < len(content):
                matched = False
                
                for token_type, pattern in self.compiled_patterns:
                    match = pattern.match(content, pos)
                    if match:
                        token_string = match.group(0)
                        
                        if token_type != 'WHITESPACE':
                            token_info = {
                                'type': token_type,
                                'line': line_num,
                                'position': pos
                            }
                            tokens.append(token_info)
                            token_types[token_type] = token_types.get(token_type, 0) + 1
                        
                        line_num += token_string.count('\n')
                        pos = match.end()
                        matched = True
                        break
                
                if not matched:
                    pos += 1
            
            return {
                'success': True,
                'tokens': tokens,
                'token_types': token_types,
                'total_tokens': len(tokens),
                'filename': filename
            }
            
        except Exception as e:
            logger.error(f"Error tokenizing CSS file {filename}: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'filename': filename
            }

class GenericTokenizer(CodeTokenizer):
    """Generic tokenizer for other file types"""
    
    def tokenize(self, content: str, filename: str) -> Dict[str, Any]:
        try:
            tokens = []
            token_types = {}
            
            # Enhanced tokenization patterns
            patterns = [
                ('KEYWORD', r'\b(?:if|else|for|while|function|class|def|return|import|export|var|let|const|public|private|static|void|int|string|boolean|true|false|null|undefined)\b'),
                ('STRING', r'"[^"]*"|\'[^\']*\'|`[^`]*`'),
                ('NUMBER', r'\b\d+(?:\.\d+)?\b'),
                ('COMMENT', r'//.*?$|/\*.*?\*/|#.*?$'),
                ('OPERATOR', r'[+\-*/%=<>!&|^~?:]+'),
                ('DELIMITER', r'[(){}\[\];,.@]'),
                ('IDENTIFIER', r'\b[a-zA-Z_]\w*\b'),
                ('WHITESPACE', r'\s+'),
            ]
            
            compiled_patterns = [(name, re.compile(pattern, re.MULTILINE | re.DOTALL)) 
                               for name, pattern in patterns]
            
            pos = 0
            line_num = 1
            
            while pos < len(content):
                matched = False
                
                for token_type, pattern in compiled_patterns:
                    match = pattern.match(content, pos)
                    if match:
                        token_string = match.group(0)
                        
                        if token_type != 'WHITESPACE':
                            token_info = {
                                'type': token_type,
                                'line': line_num,
                                'position': pos
                            }
                            tokens.append(token_info)
                            token_types[token_type] = token_types.get(token_type, 0) + 1
                        
                        line_num += token_string.count('\n')
                        pos = match.end()
                        matched = True
                        break
                
                if not matched:
                    pos += 1
            
            return {
                'success': True,
                'tokens': tokens,
                'token_types': token_types,
                'total_tokens': len(tokens),
                'filename': filename
            }
            
        except Exception as e:
            logger.error(f"Error tokenizing file {filename}: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'filename': filename
            }

def get_tokenizer(file_extension: str) -> CodeTokenizer:
    """Get appropriate tokenizer based on file extension"""
    tokenizer_map = {
        '.py': PythonTokenizer(),
        '.java': JavaTokenizer(),
        '.js': JavaScriptTokenizer(),
        '.jsx': JavaScriptTokenizer(),
        '.ts': JavaScriptTokenizer(),
        '.tsx': JavaScriptTokenizer(),
        '.html': HTMLTokenizer(),
        '.htm': HTMLTokenizer(),
        '.css': CSSTokenizer(),
        '.scss': CSSTokenizer(),
        '.sass': CSSTokenizer(),
        '.less': CSSTokenizer(),
    }
    
    return tokenizer_map.get(file_extension.lower(), GenericTokenizer())
