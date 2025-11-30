# 🤖 Job Application Bot - Assistant PFE Data Engineer

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Gemini](https://img.shields.io/badge/AI-Google%20Gemini-orange.svg)](https://ai.google.dev/)
[![LaTeX](https://img.shields.io/badge/LaTeX-PDF-green.svg)](https://www.latex-project.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Un outil d'automatisation intelligent pour personnaliser vos candidatures avec l'IA**

Cet assistant semi-automatisé utilise l'intelligence artificielle (Google Gemini) pour analyser des offres d'emploi et générer automatiquement des CV et lettres de motivation **personnalisés** en PDF de qualité professionnelle.

---

## ✨ Fonctionnalités

- 🤖 **Analyse IA** : Extraction automatique des informations clés de l'offre (entreprise, poste, compétences)
- ✍️ **Génération personnalisée** : Création de paragraphes d'accroche adaptés à chaque offre
- 📄 **PDF professionnels** : Rendu LaTeX de haute qualité
- 📊 **Suivi automatique** : Intégration Google Sheets (optionnel)
- 🔒 **100% gratuit** : Utilise uniquement des APIs gratuites
- 🎯 **Portfolio-ready** : Démontre vos compétences en Python, APIs et automatisation

---

## 🚀 Démarrage rapide

### 1. Installation

```bash
# Clonez le projet
git clone https://github.com/CaptainA10/job-application-bot.git
cd job-application-bot

# Installez les dépendances
pip install -r requirements.txt
```

### 2. Configuration

```bash
# Créez votre fichier de configuration
cp .env.example .env
```

Éditez `.env` et ajoutez votre clé API Gemini :
```env
GEMINI_API_KEY=votre_cle_ici
```

> 💡 **Obtenir une clé gratuite** : https://aistudio.google.com/

### 3. Lancement

```bash
python app.py
```

Tapez **DEMO** pour tester avec l'offre d'exemple, ou collez le texte d'une vraie offre !

---

## 📋 Prérequis

- **Python 3.8+**
- **LaTeX** (pour générer les PDF) :
  - Windows : [MiKTeX](https://miktex.org/download) ou [TeX Live](https://tug.org/texlive/)
  - Mac : `brew install --cask mactex`
  - Linux : `sudo apt-get install texlive-full`

---

## 🏗️ Architecture

```
Offre d'emploi → Gemini AI → Analyse & Extraction
                     ↓
              Génération texte personnalisé
                     ↓
              Templates Jinja2 + LaTeX
                     ↓
              PDF CV + Lettre de motivation
                     ↓
              Google Sheets (tracking)
```

**Stack Technique :**
- Backend : Python 3.8+
- IA : Google Gemini Flash API
- Templates : Jinja2
- PDF : LaTeX (pdflatex)
- Tracking : Google Sheets API (optionnel)

---

## 📁 Structure du projet

```
job-application-bot/
├── app.py                      # Script principal
├── config.py                   # Configuration
├── utils.py                    # Fonctions utilitaires
├── requirements.txt            # Dépendances Python
├── .env.example               # Template de configuration
├── templates/                 # Templates LaTeX
│   ├── template_cv.tex
│   └── template_lettre.tex
├── examples/                  # Exemples
│   └── sample_job_offer.txt
└── candidatures_genere/      # PDF générés (auto-créé)
```

---

## 🎨 Personnalisation

### Modifier vos informations

Éditez le fichier `.env` :
```env
USER_NAME=Votre Nom
USER_PROFILE=Vos compétences principales
USER_EXPERIENCE=Votre expérience clé
```

### Personnaliser les templates LaTeX

Les templates sont dans `templates/` avec des variables Jinja2 :
- `\VAR{company_name}` : Nom de l'entreprise
- `\VAR{job_title}` : Titre du poste
- `\VAR{ai_generated_paragraph}` : Texte généré par l'IA
- `\VAR{keywords}` : Mots-clés extraits

---

## 🔒 Sécurité

> **⚠️ IMPORTANT** : Ce bot **NE fait PAS de scraping automatique**. Vous copiez manuellement le texte pour éviter :
> - Le bannissement de votre compte LinkedIn
> - Les violations des conditions d'utilisation
> - Les détections anti-bot

**Protection des credentials :**
- Ne committez **JAMAIS** votre `.env` ou `credentials.json`
- Le `.gitignore` est configuré pour les exclure
- Vérifiez avant chaque `git push`

---

## 📊 Exemple de résultat

```
✓ Analyse terminée: Effidic - Stage Data Engineer
✓ Template rendu: Lettre_Gad_Nguette_Effidic.tex
✓ PDF généré: Lettre_Gad_Nguette_Effidic.pdf
✓ Template rendu: CV_Gad_Nguette_Effidic.tex
✓ PDF généré: CV_Gad_Nguette_Effidic.pdf
✓ Ajouté à Suivi_Candidatures_PFE
```

---

## 💡 Avantages pour votre portfolio

Ce projet démontre :

✅ **Data Engineering** : Pipeline ETL (extraction → transformation → chargement)  
✅ **APIs** : Intégration Google Gemini et Google Sheets  
✅ **Automatisation** : Scripting Python avancé  
✅ **Template Engineering** : Jinja2 + LaTeX  
✅ **Best Practices** : Config management, error handling, logging  
✅ **Documentation** : README complet, guides, code commenté  

---

## 🐛 Dépannage

### Erreur : `pdflatex` not found

**Solution** : LaTeX n'est pas installé ou pas dans le PATH
1. Installez MiKTeX/TeX Live
2. Redémarrez votre terminal/IDE
3. Vérifiez : `pdflatex --version`

### Erreur : No JSON found in AI response

**Solution** : L'offre est peut-être trop courte ou mal formatée. Le bot utilise des valeurs par défaut automatiquement.

### Erreur : Google Sheets API

**Solution** : Vérifiez que `credentials.json` existe et que vous avez partagé le Sheet avec l'email du Service Account. Voir [SETUP_GUIDE.md](SETUP_GUIDE.md).

---

## 📚 Documentation

- [QUICKSTART.md](QUICKSTART.md) - Démarrage en 5 minutes
- [SETUP_GUIDE.md](SETUP_GUIDE.md) - Configuration détaillée
- [LICENSE](LICENSE) - Licence MIT

---

## 🤝 Contribution

Les contributions sont bienvenues ! N'hésitez pas à :
- Signaler des bugs (Issues)
- Proposer des améliorations (Pull Requests)
- Partager vos retours d'expérience

---

## 📄 Licence

MIT License - Libre d'utilisation pour vos projets personnels et professionnels.

---

## 👤 Auteur

**Gad Nguette** - Data Engineering Student

- GitHub: [@CaptainA10](https://github.com/CaptainA10)
- Email: nguettefanegad@gmail.com

---

**⭐ Si ce projet vous aide, n'hésitez pas à mettre une étoile sur GitHub !**
