# Guide de contribution

Merci de votre intérêt pour contribuer à MeteoFrance Weather App ! 🎉

## Comment contribuer

### 1. Préparation de l'environnement

```bash
# Clonez le repository
git clone https://github.com/YoannDev90/MeteoFrance.git
cd MeteoFrance

# Créez un environnement virtuel
python -m venv .venv
source .venv/bin/activate  # Sur Windows: .venv\Scripts\activate

# Installez les dépendances de développement
pip install -e .
pip install black isort flake8 mypy pytest
```

### 2. Développement

#### Style de code

Ce projet utilise plusieurs outils pour maintenir la qualité du code :

- **Black** : Formatage automatique du code
- **isort** : Tri automatique des imports
- **flake8** : Linting et vérification de style
- **mypy** : Vérification des types

```bash
# Formatez le code
black main.py
isort main.py

# Vérifiez le style
flake8 main.py

# Vérifiez les types
mypy main.py
```

#### Structure du code

- Utilisez la classe `WeatherApp` pour encapsuler la logique
- Ajoutez des méthodes pour chaque nouvelle fonctionnalité
- Documentez vos fonctions avec des docstrings
- Utilisez des noms de variables descriptifs

### 3. Tests

```bash
# Exécutez les tests
pytest

# Avec couverture
pytest --cov=main --cov-report=html
```

### 4. Commit

Utilisez des messages de commit clairs et descriptifs :

```bash
git commit -m "feat: add new weather feature

- Add detailed description
- Explain what was changed
- Reference issues if applicable"
```

#### Types de commit

- `feat:` Nouvelle fonctionnalité
- `fix:` Correction de bug
- `docs:` Changements de documentation
- `style:` Changements de style (formatage, etc.)
- `refactor:` Refactorisation du code
- `test:` Ajout ou modification de tests
- `chore:` Tâches de maintenance

### 5. Pull Request

1. Créez une branche pour votre fonctionnalité
2. Testez vos changements
3. Mettez à jour la documentation si nécessaire
4. Ouvrez une Pull Request avec une description détaillée

## Code de conduite

- Soyez respectueux et courtois
- Fournissez des retours constructifs
- Respectez les standards de qualité du projet

## Signes de reconnaissance

Tous les contributeurs seront mentionnés dans les releases et le README.

## Questions ?

N'hésitez pas à ouvrir une issue pour poser vos questions !
