# Quick Start Guide

## 🚀 Démarrage rapide (5 minutes)

### 1. Installation des dépendances

```bash
# Installez les packages Python
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

> 💡 **Obtenir une clé gratuite :** https://aistudio.google.com/

### 3. Test avec la démo

```bash
python app.py
```

Quand demandé, tapez : **DEMO**

### 4. Vérifiez les résultats

Ouvrez le dossier `candidatures_genere/` et vérifiez les PDF générés !

---

## 📝 Utilisation réelle

1. Trouvez une offre sur LinkedIn/WTTJ
2. Copiez le texte complet de l'annonce
3. Lancez `python app.py`
4. Collez le texte
5. Appuyez sur Entrée deux fois
6. Vérifiez les PDF
7. Envoyez votre candidature 🎯

---

## 🆘 Problèmes ?

**Erreur pdflatex :**
- Installez LaTeX (voir SETUP_GUIDE.md section 1)

**Erreur API :**
- Vérifiez votre clé Gemini dans `.env`

**Plus d'aide :**
- Consultez [SETUP_GUIDE.md](SETUP_GUIDE.md)
- Section "Dépannage" dans [README.md](README.md)
