"""
Configuration management for the Job Application Bot
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration"""
    
    # API Keys
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
    
    # Google Sheets
    GOOGLE_CREDENTIALS_PATH = os.getenv('GOOGLE_CREDENTIALS_PATH', 'credentials.json')
    GOOGLE_SHEET_NAME = os.getenv('GOOGLE_SHEET_NAME', 'Suivi_Candidatures_PFE')
    
    # Directories
    OUTPUT_DIR = os.getenv('OUTPUT_DIR', 'candidatures_genere')
    TEMPLATES_DIR = 'templates'
    
    # User Profile
    USER_NAME = os.getenv('USER_NAME', 'Gad Nguette')
    USER_PROFILE = os.getenv('USER_PROFILE', 'Étudiant Data Engineer, stack : SQL, dbt, Python, BigQuery')
    USER_EXPERIENCE = os.getenv('USER_EXPERIENCE', 'Stage chez LIKA Consulting en Data Engineering')
    
    # Gemini Model
    GEMINI_MODEL = 'gemini-flash-latest'
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        errors = []
        
        if not cls.GEMINI_API_KEY:
            errors.append("GEMINI_API_KEY is not set. Get one at https://aistudio.google.com/")
        
        if not os.path.exists(cls.OUTPUT_DIR):
            os.makedirs(cls.OUTPUT_DIR)
            print(f"✓ Created output directory: {cls.OUTPUT_DIR}")
        
        if errors:
            raise ValueError("\n".join(errors))
        
        return True
