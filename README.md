```
▄▀▄
   █████╗  ██╗ ███╗   ███╗ ███████╗ ███████╗
  ██╔══██╗ ██║ ████╗ ████║ ██╔════╝ ██╔════╝
  ███████║ ██║ ██╔████╔██║ █████╗   █████╗  
  ██╔══██║ ██║ ██║╚██╔╝██║ ██╔════╝ ██╔════╝
  ██║  ██║ ██║ ██║ ╚═╝ ██║ ███████╗ ███████╗
  ╚═╝  ╚═╝ ╚═╝ ╚═╝     ╚═╝ ╚══════╝ ╚══════╝
```

# HotelManager

Application desktop de gestion hôtelière développée avec **PyQt5** et **MariaDB**.

## Fonctionnalités

- **Gestion des clients** — Inscription, modification, suppression et archivage des clients de l'hôtel
- **Attribution de chambres** — Attribution automatique de chambres avec vérification de disponibilité
- **Gestion des employés** — Recrutement, promotion, enregistrement des absences et traitement des paiements
- **Système de salaires** — Calcul automatique des salaires selon le poste et le grade
- **Historique et archivage** — Les clients supprimés sont archivés pour conservation des traces
- **Export CSV** — Exportation des données clients et de l'historique en fichiers CSV
- **Recherche** — Recherche en temps réel avec requêtes SQL sur les clients, l'historique et les employés

## Stack technique

| Couche | Technologie |
|-------|-----------|
| Interface graphique | PyQt5 (Qt5) |
| Base de données | MariaDB (via connecteur `mariadb`) |
| Export de données | pandas |
| Configuration | python-dotenv |
| Tests | unittest |

## Installation

```bash
# Créer un environnement virtuel
python -m venv .venv
source .venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Configurer la base de données
cp .env.example .env
# Modifier .env avec vos identifiants MariaDB

# Exécuter
python main.py
```

## Exécution des tests

```bash
python -m unittest discover -s tests -v
```

## Structure du projet

```
HotelManager/
├── main.py                  # Point d'entrée de l'application
├── db/
│   ├── config.py            # Configuration BD + constantes salariales
│   ├── connection.py        # Connexion partagée à la BD
│   ├── database_clients.py  # CRUD clients + opérations de recherche
│   └── database_employees.py # CRUD employés + opérations de recherche
├── ui/
│   ├── main_window.py       # Configuration de la fenêtre principale et gestion des événements
│   ├── employee_manager.py  # Gestionnaires d'actions des employés
│   ├── paiement.py          # Dialogue de paiement
│   ├── recrutement.py       # Dialogue de recrutement
│   └── interface.ui         # Définition UI Qt Designer
├── modules/
│   ├── crud.py              # Logique d'ajout/modification/suppression des clients
│   ├── display.py           # Affichage des tableaux et gestionnaires de sélection
│   └── form.py              # Extraction et validation des données de formulaire
├── utils/
│   ├── helpers.py           # Fonctions utilitaires de validation
│   └── employee_utils.py    # Fonctions utilitaires pour les employés
├── tests/
│   ├── test_config.py       # Tests de configuration et salaires
│   ├── test_helpers.py      # Tests de logique de validation
│   └── test_employee_utils.py # Tests des utilitaires employés
├── .env.example             # Modèle de variables d'environnement
├── .gitignore               # Règles d'ignorance git
├── requirements.txt         # Dépendances Python
└── README.md
```

## Schéma de la base de données

L'application crée automatiquement les tables suivantes :

- **`clients`** — Réservations des clients de l'hôtel (nom, CIN, chambre, dates, prix)
- **`clients_archive`** — Enregistrements clients archivés (supprimés)
- **`employees`** — Personnel (nom, poste, salaire, grade, absences)

## Auteur

Randrianandrasana Jean Aime