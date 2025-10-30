# MeteoFrance Weather App

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![CI](https://github.com/yoann/MeteoFrance/actions/workflows/ci.yml/badge.svg)](https://github.com/yoann/MeteoFrance/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/yoann/MeteoFrance/branch/main/graph/badge.svg)](https://codecov.io/gh/yoann/MeteoFrance)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Une application météo complète utilisant l'API MeteoFrance pour obtenir des prévisions météorologiques détaillées en France.

## ✨ Fonctionnalités

- **Prévisions actuelles** : Température, humidité, vent, précipitations
- **Prévisions horaires** : 24 heures de prévisions détaillées
- **Prévisions quotidiennes** : 14 jours de prévisions
- **Observations météo** : Données des stations météo locales
- **Image du jour** : Photos satellites et descriptions météo
- **Alertes météo** : Avertissements officiels par département
- **Prévisions de pluie** : Prévisions de pluie précises
- **Graphiques** : Visualisation des températures horaires
- **Favoris** : Sauvegarde de vos villes préférées
- **Configuration** : Unités personnalisables (Celsius/Fahrenheit, km/h/mph, mm/inches)
- **Cache** : Mise en cache des données pour de meilleures performances

## 🚀 Installation

### Prérequis

- Python 3.8 ou supérieur
- pip

### Installation depuis PyPI (recommandé)

```bash
pip install meteofrance-app
```

### Installation depuis les sources

```bash
# Clonez le repository
git clone https://github.com/YoannDev90/MeteoFrance.git
cd MeteoFrance

# Installez en mode développement
pip install -e .
```

### Installation manuelle

```bash
# Installez les dépendances requises
pip install meteofrance-api toml matplotlib
```

## 📖 Utilisation

### Lancement de l'application

```bash
python main.py
```

### Interface utilisateur

L'application présente un menu interactif :

1. **Villes favorites** : Sélectionnez une ville sauvegardée
2. **Nouvelle ville** : Recherchez et ajoutez une nouvelle ville

### Configuration

Modifiez le fichier `config.toml` pour personnaliser les unités :

```toml
[units]
temperature = "C"  # ou "F"
wind_speed = "km/h"  # ou "mph"
precipitation = "mm"  # ou "in"
```

### Fichiers générés

- `favorites.json` : Vos villes favorites
- `weather_graph.png` : Graphiques de température (optionnel)

## 🏗️ Architecture

L'application est structurée en classe `WeatherApp` avec les méthodes suivantes :

- `load_config()` / `save_favorites()` : Gestion de la configuration
- `get_cached_forecast()` : Récupération avec cache
- `display_*()` : Méthodes d'affichage pour chaque section
- `convert_*()` : Conversion d'unités
- `run()` : Boucle principale de l'application

## 🔧 Développement

### Préparation de l'environnement

```bash
# Installez les outils de développement
pip install black isort flake8 mypy pre-commit

# Configurez pre-commit
pre-commit install
```

### Structure du projet

```
MeteoFrance/
├── main.py              # Application principale
├── config.toml          # Configuration des unités
├── requirements.txt     # Dépendances Python
├── pyproject.toml       # Configuration du package
├── .gitignore          # Fichiers ignorés par Git
├── .pre-commit-config.yaml  # Configuration pre-commit
├── .github/
│   └── workflows/       # Workflows GitHub Actions
├── LICENSE             # License MIT
├── README.md           # Documentation
└── CONTRIBUTING.md     # Guide de contribution
```

### Tests

```bash
# Exécutez les tests (si implémentés)
python -m pytest

# Vérifiez la qualité du code
pre-commit run --all-files
```

### Contribution

1. Fork le projet
2. Créez une branche pour votre fonctionnalité (`git checkout -b feature/AmazingFeature`)
3. Committez vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

Voir [CONTRIBUTING.md](CONTRIBUTING.md) pour plus de détails.

## 👥 Contributeurs

- **Yoann** - *Développeur principal* - [GitHub](https://github.com/yoann)

## 🙏 Remerciements

- [MeteoFrance](https://www.meteofrance.fr/) pour l'API
- [meteofrance-api](https://github.com/hacf-fr/meteofrance-api) pour le client Python
- [Matplotlib](https://matplotlib.org/) pour les graphiques
- Toute la communauté open source

## 📋 API MeteoFrance

Cette application utilise l'API officielle de MeteoFrance pour :

- Prévisions météorologiques
- Observations des stations
- Images satellites
- Alertes météorologiques
- Données pluviométriques

## ⚖️ License

Ce projet est sous license MIT - voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 🙏 Remerciements

- [MeteoFrance](https://www.meteofrance.fr/) pour l'API
- [meteofrance-api](https://github.com/hacf-fr/meteofrance-api) pour le client Python
- Communauté open source

---

**Note** : Cette application est un outil éducatif et ne remplace pas les services officiels de MeteoFrance pour des usages critiques.
