# 🏦 BIGO BANK — Hexagonal Architecture Bank App

💡 Description :BIGO BANK est une application de gestion de comptes bancaires développée dans une architecture hexagonale (ports & adapters).
Elle simule les opérations d’un client bancaire : création de comptes, dépôts, retraits, gestion de découvert, plafonds d’épargne et génération de relevés mensuels.

L’objectif du projet est de démontrer une architecture propre, maintenable et testable, tout en proposant un front moderne en React.

# ⚙️ Stack technique

- Backend : Python 3.11, FastAPI — framework web rapide et typé
- SQLAlchemy — ORM pour la persistance SQLite
- Pydantic — validation et sérialisation
- pytest — tests unitaires
- Docker / docker-compose — pour l’exécution isolée
- Frontend : React + Vite, Vanilla CSS (sans Tailwind)
- Base de données : SQLite (fichier bank.db)

# 🧱 Architecture (DDD + Hexagonale)

bank_account/
├── domain/              # Règles métier
│   ├── models.py        # Entités : BankAccount, Operation
│   ├── exceptions.py    # Erreurs métier
│   └── __init__.py
│
├── application/         # Cas d’usage / logique applicative
│   ├── services.py      # Dépôts, retraits, création de comptes
│   ├── dto.py           # Objets de transfert
│   └── __init__.py
│
├── infrastructure/      # Connecteurs et adapters
│   ├── api/             # Routes FastAPI
│   │   └── routes.py
│   └── persistence/     # SQLAlchemy ORM
│       ├── db.py
│       ├── orm_models.py
│       └── repositories.py
│
├── main.py              # Point d’entrée FastAPI
└── tests/               # Tests unitaires

🧩 L’application sépare clairement le domaine, la logique d’application et l’infrastructure,ce qui facilite l’évolution et les tests unitaires.

# 💰 Fonctionnalités (features)

- 🏦 Feature 1 : Compte bancaire

1- Création d’un compte avec numéro unique et solde
2- Dépôt et retrait d’argent
Règle : un retrait ne peut pas dépasser le solde disponible

- 💳 Feature 2 : Découvert autorisé

1- Possibilité de définir un découvert maximum
2- Règle : un retrait est autorisé si le solde final ≥ –découvert

- 💸 Feature 3 : Livret épargne

1- Plafond de dépôt configuré
2- Aucun découvert possible

Deux types de livrets : Compte courant, Livret B

- 📄 Feature 4 : Relevé de compte

1- Relevé mensuel des opérations (triées par date décroissante)
2- Affichage des opérations dans une modale

🚀 Exécution du projet
▶️ 1. Lancer le backend (FastAPI)

Depuis la racine du projet :

# Activer l'environnement virtuel

.venv\Scripts\activate

# Lancer l'API

uvicorn bank_account.main:app --reload

- L’API sera accessible sur : -> http://127.0.0.1:8000
- Documentation interactive Swagger : -> http://127.0.0.1:8000/docs

# 🖥️ 2. Lancer le frontend (React)

Depuis le dossier bank-account-ui :

- npm install
- npm run dev

Le front sera accessible sur : -> http://localhost:5173

# 🧩 3. Avec Docker

Depuis la racine du projet : docker compose up --build
Cela lancera : Le backend FastAPI sur le port 8000, et le frontend React sur le port 5173

# 🧪 Tests

Exécuter les tests unitaires du backend : pytest -v

# 📁 Exemple d’utilisation

1- Créer un compte courant avec ou sans découvert.
2- Créer un livret épargne avec un plafond.
3- Faire un dépôt / retrait.
4- Consulter le relevé (et le télécharger en PDF). (à faire)

# 🧠 Auteur: 👨‍💻 Maël Hounche

Projet technique et pédagogique réalisé dans le cadre de la démonstration de compétences logicielles et de modélisation métier (architecture hexagonale + React + FastAPI).
