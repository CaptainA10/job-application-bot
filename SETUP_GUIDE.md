# 📚 Guide de Configuration Détaillé

Ce guide vous accompagne pas à pas dans la configuration complète du Job Application Bot.

## 🔧 Table des matières

1. [Installation de LaTeX](#1-installation-de-latex)
2. [Obtention de la clé Gemini API](#2-obtention-de-la-clé-gemini-api)
3. [Configuration Google Sheets (Optionnel)](#3-configuration-google-sheets-optionnel)
4. [Premier lancement](#4-premier-lancement)
5. [Personnalisation avancée](#5-personnalisation-avancée)

---

## 1. Installation de LaTeX

LaTeX est nécessaire pour générer les PDF de haute qualité.

### Windows

**Option A : TeX Live (Recommandé)**

1. Téléchargez l'installateur : https://tug.org/texlive/acquire-netinstall.html
2. Lancez `install-tl-windows.exe`
3. Choisissez l'installation complète (environ 7 GB)
4. Attendez la fin (30-60 minutes selon connexion)
5. Vérifiez l'installation :
   ```powershell
   pdflatex --version
   ```

**Option B : MiKTeX (Plus léger)**

1. Téléchargez : https://miktex.org/download
2. Installez avec les paramètres par défaut
3. À la première compilation, MiKTeX téléchargera les packages manquants

### Mac

```bash
# Avec Homebrew (4-5 GB)
brew install --cask mactex

# Ou version basique (plus légère)
brew install --cask basictex

# Ajoutez au PATH
export PATH="/Library/TeX/texbin:$PATH"

# Vérifiez
pdflatex --version
```

### Linux (Ubuntu/Debian)

```bash
# Installation complète
sudo apt-get update
sudo apt-get install texlive-full texlive-lang-french

# Ou installation minimale
sudo apt-get install texlive texlive-latex-extra texlive-lang-french

# Vérifiez
pdflatex --version
```

---

## 2. Obtention de la clé Gemini API

Google Gemini offre un tier gratuit très généreux (60 requêtes/minute).

### Étapes détaillées

1. **Accédez à Google AI Studio**
   
   Ouvrez : https://aistudio.google.com/

2. **Connectez-vous**
   
   Utilisez votre compte Google (personnel ou professionnel)

3. **Créez une clé API**
   
   - Cliquez sur "Get API Key" dans le menu de gauche
   - Puis "Create API Key"
   - Sélectionnez "Create API key in new project" (ou un projet existant)
   - Copiez la clé générée (commence par `AIza...`)

4. **Ajoutez la clé à votre projet**
   
   Éditez le fichier `.env` :
   ```env
   GEMINI_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXX
   ```

> [!IMPORTANT]
> **Protégez votre clé API !**
> - Ne la partagez jamais publiquement
> - Ne la committez pas sur GitHub
> - Régénérez-la si elle est compromise

### Limites du tier gratuit

- **15 requêtes/minute** (largement suffisant)
- **1 500 requêtes/jour**
- **1 million tokens/jour**

Pour notre usage : ~10-20 candidatures/jour → **largement dans les limites** ✅

---

## 3. Configuration Google Sheets (Optionnel)

Google Sheets permet de tracker automatiquement vos candidatures.

### 3.1 Créer le Google Sheet

1. Allez sur https://sheets.google.com
2. Créez un nouveau sheet nommé **"Suivi_Candidatures_PFE"**
3. Dans la première ligne (header), ajoutez :
   ```
   Date | Entreprise | Poste | Statut | Lien
   ```

### 3.2 Activer l'API Google Sheets

1. **Accédez à Google Cloud Console**
   
   https://console.cloud.google.com/

2. **Créez un projet**
   
   - Cliquez sur "Select a project" → "New Project"
   - Nom : "Job Application Bot"
   - Cliquez "Create"

3. **Activez les APIs**
   
   - Menu "APIs & Services" → "Enable APIs and Services"
   - Recherchez et activez :
     - **Google Sheets API**
     - **Google Drive API**

4. **Créez un Service Account**
   
   - Menu "APIs & Services" → "Credentials"
   - "Create Credentials" → "Service Account"
   - Nom : "job-bot-service"
   - Role : "Editor"
   - Cliquez "Done"

5. **Téléchargez les credentials**
   
   - Cliquez sur le Service Account créé
   - Onglet "Keys" → "Add Key" → "Create new key"
   - Format : **JSON**
   - Téléchargez le fichier

6. **Placez les credentials**
   
   - Renommez le fichier en `credentials.json`
   - Placez-le à la racine du projet job-application-bot/
   - **Ne le committez PAS sur Git !** (déjà dans .gitignore)

### 3.3 Partagez le Sheet avec le Service Account

1. Ouvrez le fichier `credentials.json`
2. Copiez la valeur de `"client_email"` (format : xxx@xxx.iam.gserviceaccount.com)
3. Dans votre Google Sheet, cliquez "Partager"
4. Ajoutez cet email avec droit "Éditeur"

### 3.4 Configurez le nom du Sheet

Dans `.env` :
```env
GOOGLE_SHEET_NAME=Suivi_Candidatures_PFE
GOOGLE_CREDENTIALS_PATH=credentials.json
```

---

## 4. Premier lancement

### Test avec l'offre démo

```bash
# Lancez l'application
python app.py

# À l'invite, tapez : DEMO
DEMO

# Le bot va :
# 1. Charger l'offre d'exemple (Effidic)
# 2. L'analyser avec Gemini
# 3. Générer les PDF
# 4. (Si configuré) Ajouter au Sheet
```

### Vérifiez les résultats

```bash
# Listez les fichiers générés
ls candidatures_genere/

# Vous devriez voir :
# - CV_Gad_Nguette_Effidic.pdf
# - Lettre_Gad_Nguette_Effidic.pdf
# - CV_Gad_Nguette_Effidic.tex
# - Lettre_Gad_Nguette_Effidic.tex
# - Fichiers .aux, .log (LaTeX)
```

Ouvrez les PDF et vérifiez la qualité !

---

## 5. Personnalisation avancée

### 5.1 Vos informations personnelles

Éditez `.env` :

```env
USER_NAME=Votre Nom Complet
USER_PROFILE=Étudiant Data Analyst, stack : Python, R, Power BI, SQL Server
USER_EXPERIENCE=Stage chez XXX en analyse de données, projet de data viz avec D3.js
```

### 5.2 Modifier le template de lettre

Le fichier `templates/template_lettre.tex` utilise Jinja2 avec des délimiteurs spéciaux :

```latex
% Variable simple
\VAR{company_name}

% Bloc conditionnel
\BLOCK{if keywords}
Je maîtrise \VAR{keywords[0]}
\BLOCK{endif}
```

**Ajoutez vos propres sections** :
- Votre adresse complète
- Votre téléphone
- Votre LinkedIn/GitHub

Exemple :
```latex
\address{%
Gad Nguette\\
15 Rue de la Data\\
75001 Paris\\
+33 6 12 34 56 78\\
gad.nguette@example.com
}
```

### 5.3 Modifier le template de CV

Dans `templates/template_cv.tex`, personnalisez :

1. **La section Expérience** : Ajoutez vos vrais stages
2. **La section Projets** : Vos projets GitHub
3. **Les compétences** : Votre stack réelle

### 5.4 Améliorer le prompt IA

Dans `app.py`, fonction `analyze_job_offer()`, modifiez le prompt pour :

- Changer le ton (plus formel/décontracté)
- Ajouter des éléments spécifiques à mettre en avant
- Demander plus de mots-clés

Exemple :
```python
prompt = f"""
...
Mon profil :
- Nom : {Config.USER_NAME}
- Compétences : {Config.USER_PROFILE}
- Expérience : {Config.USER_EXPERIENCE}
- Projet phare : Mon bot d'automatisation de candidatures (ce projet !)
...
"""
```

---

## ✅ Checklist de configuration

- [ ] Python 3.8+ installé
- [ ] LaTeX installé (`pdflatex` dans le PATH)
- [ ] Dépendances Python installées (`pip install -r requirements.txt`)
- [ ] Fichier `.env` créé et configuré
- [ ] Clé Gemini API obtenue et ajoutée
- [ ] (Optionnel) Google Sheets configuré
- [ ] (Optionnel) `credentials.json` téléchargé et placé
- [ ] Test avec `python app.py` + `DEMO` réussi
- [ ] PDF générés et vérifiés

---

## 🆘 Besoin d'aide ?

### Problèmes courants

**Q : `ModuleNotFoundError: No module named 'google.generativeai'`**

R : Installez les dépendances :
```bash
pip install -r requirements.txt
```

**Q : `pdflatex: command not found`**

R : LaTeX n'est pas installé ou pas dans le PATH. Voir section 1.

**Q : Les PDF contiennent `\VAR{...}` littéralement**

R : Problème de délimiteurs Jinja2. Vérifiez que les templates utilisent `\VAR{}` et non `{{ }}`.

**Q : Erreur Google Sheets "Permission denied"**

R : Vérifiez que vous avez bien partagé le Sheet avec l'email du Service Account.

---

**🎉 Vous êtes prêt ! Lancez `python app.py` et bonne chance pour vos candidatures !**
