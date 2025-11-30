"""
Utility functions for the Job Application Bot
"""
import os
import re
import json
import subprocess
from typing import Dict, Optional

def extract_json_from_ai_response(response_text: str) -> Optional[Dict]:
    """
    Extract and parse JSON from AI response that may contain markdown or extra text.
    
    Args:
        response_text: Raw response from AI model
        
    Returns:
        Parsed JSON as dictionary, or None if parsing fails
    """
    try:
        # Try to find JSON block in markdown code blocks
        json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', response_text, re.DOTALL)
        if json_match:
            json_str = json_match.group(1)
        else:
            # Try to find raw JSON object
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
            else:
                print("⚠ No JSON found in AI response")
                return None
        
        # Parse JSON
        data = json.loads(json_str)
        return data
        
    except json.JSONDecodeError as e:
        print(f"⚠ JSON parsing error: {e}")
        print(f"Response text: {response_text[:200]}...")
        return None
    except Exception as e:
        print(f"⚠ Unexpected error extracting JSON: {e}")
        return None


def compile_latex_to_pdf(tex_file: str, output_dir: str) -> bool:
    """
    Compile LaTeX file to PDF using pdflatex.
    
    Args:
        tex_file: Path to the .tex file
        output_dir: Directory for output files
        
    Returns:
        True if compilation succeeded, False otherwise
    """
    try:
        # Run pdflatex twice for proper references
        for _ in range(2):
            result = subprocess.run(
                ['pdflatex', '-interaction=nonstopmode', f'-output-directory={output_dir}', tex_file],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                print(f"⚠ LaTeX compilation warning (exit code {result.returncode})")
                # Continue anyway as pdflatex often returns non-zero even on success
        
        # Check if PDF was created
        pdf_file = tex_file.replace('.tex', '.pdf')
        if os.path.exists(pdf_file):
            print(f"✓ PDF généré avec succès: {os.path.basename(pdf_file)}")
            return True
        else:
            print(f"✗ Erreur: PDF non créé")
            return False
            
    except FileNotFoundError:
        print("✗ Erreur: pdflatex n'est pas installé ou n'est pas dans le PATH")
        print("  Installez TeX Live (Windows/Linux) ou MacTeX (Mac)")
        return False
    except subprocess.TimeoutExpired:
        print("✗ Erreur: Compilation LaTeX timeout (>30s)")
        return False
    except Exception as e:
        print(f"✗ Erreur lors de la compilation: {e}")
        return False


def sanitize_filename(text: str) -> str:
    """
    Clean text to make it safe for use in filenames.
    
    Args:
        text: Input text
        
    Returns:
        Sanitized text safe for filenames
    """
    # Remove or replace invalid characters
    text = re.sub(r'[<>:"/\\|?*]', '', text)
    # Replace spaces with underscores
    text = text.replace(' ', '_')
    # Limit length
    return text[:50]


def format_date(date_str: str) -> str:
    """
    Format date string for French documents.
    
    Args:
        date_str: Date in various formats
        
    Returns:
        Formatted date string
    """
    from datetime import datetime
    
    try:
        if isinstance(date_str, str):
            dt = datetime.fromisoformat(date_str)
        else:
            dt = date_str
        
        # French month names
        months = [
            'janvier', 'février', 'mars', 'avril', 'mai', 'juin',
            'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre'
        ]
        
        return f"{dt.day} {months[dt.month - 1]} {dt.year}"
    except:
        return date_str
