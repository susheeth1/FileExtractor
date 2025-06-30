from app import db
from datetime import datetime

class ProcessedFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(50), nullable=False)
    source_type = db.Column(db.String(20), nullable=False)  # 'zip' or 'github'
    source_url = db.Column(db.Text)
    tokens_count = db.Column(db.Integer, default=0)
    processed_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ProcessedFile {self.filename}>'

class TokenizedContent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    processed_file_id = db.Column(db.Integer, db.ForeignKey('processed_file.id'), nullable=False)
    tokens = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    processed_file = db.relationship('ProcessedFile', backref=db.backref('tokenized_content', lazy=True))
    
    def __repr__(self):
        return f'<TokenizedContent {self.id}>'
