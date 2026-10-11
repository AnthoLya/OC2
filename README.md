# Projet OC2 - Scraping

Ce programme permet de récupérer les données du site Books to Scrape.
Avec utils où j'y ai mis mes fonctions, on aura un dossier data de créé, contenant un dossier images.
Dans Data on retrouvera le CSV de chaques caterogies tandis que data regroupera toutes les images des livres.

## Installation de l'environnement virtuel :

### Créer l'environnement virtuel :

```bash
python3 -m venv .venv
```
### Verifier la création de l'environnement :

```bash
ls -la .venv/
```


### Activer l'environnement virtuel sous windows :
```bash
.venv\Scripts\activate
```

### Activer l'environnement virtuel sous Linus/macOS :
```bash
source .venv/bin/activate
#Vous devez voir (.venv.) dans votre console.
```

## Installation des modules :
```bash
pip install -r requirements.txt
```

## Excecution du code : 
```bash
python main.py
```
