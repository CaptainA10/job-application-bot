"""
Job Application Bot - Automated Application Assistant
Analyzes job offers with AI and generates personalized CVs and cover letters
"""
import os
import sys
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
import google.generativeai as genai

from config import Config
from utils import extract_json_from_ai_response, compile_latex_to_pdf, sanitize_filename

# Optional: Google Sheets integration
try:
    import gspread
    from oauth2client.service_account import ServiceAccountCredentials
    SHEETS_AVAILABLE = True
except ImportError:
    SHEETS_AVAILABLE = False
    print("⚠ Google Sheets libraries not available. Install with: pip install gspread oauth2client")


class JobApplicationBot:
    """Main bot class for job application automation"""
    
    def __init__(self):
        """Initialize the bot with configuration"""
        # Validate configuration
        try:
            Config.validate()
        except ValueError as e:
            print(f"✗ Configuration error:\n{e}")
            sys.exit(1)
        
        # Configure Gemini API
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(Config.GEMINI_MODEL)
        
        # Setup Jinja2 environment with custom delimiters for LaTeX
        self.jinja_env = Environment(
            loader=FileSystemLoader(Config.TEMPLATES_DIR),
            block_start_string=r'\BLOCK{',
            block_end_string='}',
            variable_start_string=r'\VAR{',
            variable_end_string='}',
            comment_start_string=r'\#{',
            comment_end_string='}',
            trim_blocks=True,
            autoescape=False
        )
        
        print("✓ Bot initialisé avec succès")
    
    def analyze_job_offer(self, job_text: str) -> dict:
        """
        Analyze job offer using Gemini AI
        
        Args:
            job_text: Full text of the job offer
            
        Returns:
            Dictionary with extracted information and AI-generated content
        """
        print("\n🤖 Analyse de l'offre avec Gemini AI...")
        
        prompt = f"""
Tu es un expert en recrutement Data Engineering. Voici une offre de stage/emploi :

{job_text}

Mon profil :
- Nom : {Config.USER_NAME}
- Compétences : {Config.USER_PROFILE}
- Expérience : {Config.USER_EXPERIENCE}

Tâche :
1. Extrais les informations suivantes de l'offre :
   - Nom de l'entreprise
   - Titre du poste
   - Adresse de l'entreprise (si trouvée, sinon "Siège Social")
   
2. Rédige un paragraphe d'accroche personnalisé (en français, 4-5 lignes) pour une lettre de motivation qui :
   - Lie mon expérience spécifique aux besoins de cette offre
   - Mentionne des technologies ou méthodes spécifiques de l'offre
   - Montre ma motivation pour ce poste précis
   
3. Génère un paragraphe de profil professionnel (2-3 lignes) qui met en avant les compétences recherchées dans cette offre

4. Suggère 3 mots-clés techniques de l'offre à mettre en avant dans le CV

Réponds UNIQUEMENT au format JSON strict (sans texte avant ou après) :
{{
    "company": "Nom de l'entreprise",
    "title": "Titre du poste",
    "address": "Adresse complète",
    "hook_paragraph": "Paragraphe d'accroche pour la lettre...",
    "profile_paragraph": "Paragraphe de profil pour le CV...",
    "keywords": ["mot-clé 1", "mot-clé 2", "mot-clé 3"]
}}
"""
        
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text
            
            # Extract JSON from response
            data = extract_json_from_ai_response(response_text)
            
            if not data:
                print("⚠ Impossible d'extraire les données. Utilisation de valeurs par défaut.")
                return self._get_default_data()
            
            print(f"✓ Analyse terminée: {data.get('company', 'N/A')} - {data.get('title', 'N/A')}")
            return data
            
        except Exception as e:
            print(f"✗ Erreur lors de l'analyse IA: {e}")
            return self._get_default_data()
    
    def _get_default_data(self) -> dict:
        """Return default data structure when AI analysis fails"""
        return {
            "company": "Entreprise",
            "title": "Data Engineer",
            "address": "Adresse",
            "hook_paragraph": "Votre offre correspond parfaitement à mon profil de Data Engineer.",
            "profile_paragraph": "Data Engineer avec expérience en Modern Data Stack.",
            "keywords": ["Python", "SQL", "BigQuery"]
        }
    
    def generate_documents(self, data: dict, user_info: dict = None) -> tuple:
        """
        Generate CV and cover letter PDFs
        
        Args:
            data: Extracted job offer data from AI analysis
            user_info: Optional user information override
            
        Returns:
            Tuple of (cv_pdf_path, letter_pdf_path)
        """
        print("\n📄 Génération des documents...")
        
        # Prepare context for templates
        context = {
            # Job info
            "company_name": data.get("company", "Entreprise"),
            "company_address": data.get("address", "Adresse"),
            "job_title": data.get("title", "Data Engineer"),
            
            # AI-generated content
            "ai_generated_paragraph": data.get("hook_paragraph", ""),
            "ai_generated_profile": data.get("profile_paragraph", ""),
            "keywords": data.get("keywords", []),
            
            # User info
            "user_name": user_info.get("name", Config.USER_NAME) if user_info else Config.USER_NAME,
            "user_email": user_info.get("email", "nguettefanegad@gmail.com") if user_info else "nguettefanegad@gmail.com",
            "user_phone": user_info.get("phone", "+33 6 XX XX XX XX") if user_info else "+33 6 XX XX XX XX",
            "user_address": user_info.get("address", "Votre Adresse") if user_info else "Votre Adresse",
            "user_linkedin": user_info.get("linkedin", "linkedin.com/in/gad-nguette") if user_info else "linkedin.com/in/gad-nguette",
            "user_github": user_info.get("github", "github.com/CaptainA10") if user_info else "github.com/CaptainA10",
            
            # Date
            "date_today": datetime.now().strftime("%d/%m/%Y")
        }
        
        # Generate safe filename base
        company_safe = sanitize_filename(data.get("company", "Entreprise"))
        
        # Generate cover letter
        letter_filename = f"Lettre_{Config.USER_NAME.replace(' ', '_')}_{company_safe}"
        self._render_and_compile("template_lettre.tex", context, letter_filename)
        
        # Generate CV
        cv_filename = f"CV_{Config.USER_NAME.replace(' ', '_')}_{company_safe}"
        self._render_and_compile("template_cv.tex", context, cv_filename)
        
        # Return paths to generated PDFs
        letter_pdf = os.path.join(Config.OUTPUT_DIR, f"{letter_filename}.pdf")
        cv_pdf = os.path.join(Config.OUTPUT_DIR, f"{cv_filename}.pdf")
        
        return (cv_pdf, letter_pdf)
    
    def _render_and_compile(self, template_name: str, context: dict, output_filename: str):
        """Render Jinja2 template and compile to PDF"""
        try:
            # Load and render template
            template = self.jinja_env.get_template(template_name)
            rendered_tex = template.render(context)
            
            # Write .tex file
            tex_path = os.path.join(Config.OUTPUT_DIR, f"{output_filename}.tex")
            with open(tex_path, "w", encoding="utf-8") as f:
                f.write(rendered_tex)
            
            print(f"  ✓ Template rendu: {output_filename}.tex")
            
            # Compile to PDF
            compile_latex_to_pdf(tex_path, Config.OUTPUT_DIR)
            
        except Exception as e:
            print(f"  ✗ Erreur lors de la génération de {output_filename}: {e}")
    
    def add_to_sheets(self, data: dict, job_url: str = ""):
        """
        Add application to Google Sheets tracker
        
        Args:
            data: Job offer data
            job_url: URL of the job posting
        """
        if not SHEETS_AVAILABLE:
            print("\n⚠ Google Sheets non disponible (bibliothèques manquantes)")
            return
        
        if not os.path.exists(Config.GOOGLE_CREDENTIALS_PATH):
            print(f"\n⚠ Fichier credentials.json non trouvé à {Config.GOOGLE_CREDENTIALS_PATH}")
            print("  Créez un Service Account sur Google Cloud Console")
            return
        
        try:
            print("\n📊 Ajout à Google Sheets...")
            
            # Authenticate
            scope = ['https://spreadsheets.google.com/feeds',
                    'https://www.googleapis.com/auth/drive']
            creds = ServiceAccountCredentials.from_json_keyfile_name(
                Config.GOOGLE_CREDENTIALS_PATH, scope)
            client = gspread.authorize(creds)
            
            # Open sheet
            sheet = client.open(Config.GOOGLE_SHEET_NAME).sheet1
            
            # Prepare row
            row = [
                datetime.now().strftime("%d/%m/%Y"),
                data.get("company", "N/A"),
                data.get("title", "N/A"),
                "À envoyer",
                job_url
            ]
            
            # Append row
            sheet.append_row(row)
            print(f"✓ Ajouté à {Config.GOOGLE_SHEET_NAME}")
            
        except Exception as e:
            print(f"✗ Erreur Google Sheets: {e}")


def main():
    """Main application entry point"""
    print("=" * 60)
    print("   JOB APPLICATION BOT - Assistant PFE Data Engineer")
    print("=" * 60)
    
    # Initialize bot
    bot = JobApplicationBot()
    
    # Get job offer from user
    print("\n📋 ÉTAPE 1 : Saisie de l'offre d'emploi")
    print("-" * 60)
    print("Collez le texte complet de l'offre ci-dessous.")
    print("Appuyez sur Entrée deux fois pour terminer, ou tapez 'DEMO' pour utiliser un exemple.")
    print()
    
    lines = []
    empty_count = 0
    
    while True:
        try:
            line = input()
            if line.strip().upper() == 'DEMO':
                # Load demo job offer
                demo_path = os.path.join('examples', 'sample_job_offer.txt')
                if os.path.exists(demo_path):
                    with open(demo_path, 'r', encoding='utf-8') as f:
                        lines = [f.read()]
                    print("✓ Offre de démonstration chargée")
                    break
                else:
                    print("⚠ Fichier de démo non trouvé, continuez la saisie")
                    continue
            
            if not line.strip():
                empty_count += 1
                if empty_count >= 2:
                    break
            else:
                empty_count = 0
                lines.append(line)
        except EOFError:
            break
    
    job_text = "\n".join(lines).strip()
    
    if not job_text:
        print("✗ Aucune offre saisie. Arrêt.")
        return
    
    print(f"\n✓ Offre reçue ({len(job_text)} caractères)")
    
    # Analyze job offer
    data = bot.analyze_job_offer(job_text)
    
    # Generate documents
    cv_pdf, letter_pdf = bot.generate_documents(data)
    
    # Ask for job URL
    print("\n🔗 URL de l'offre (optionnel, Entrée pour passer) :")
    job_url = input().strip()
    
    # Add to Google Sheets
    bot.add_to_sheets(data, job_url)
    
    # Summary
    print("\n" + "=" * 60)
    print("✓ TERMINÉ !")
    print("=" * 60)
    print(f"Entreprise : {data.get('company', 'N/A')}")
    print(f"Poste      : {data.get('title', 'N/A')}")
    print(f"\nDocuments générés dans '{Config.OUTPUT_DIR}/' :")
    print(f"  - CV     : {os.path.basename(cv_pdf)}")
    print(f"  - Lettre : {os.path.basename(letter_pdf)}")
    print("\n💡 Vérifiez les PDF avant envoi !")
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✗ Interruption utilisateur. Au revoir !")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Erreur inattendue: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
