# 📡 Bibind - `op_bootstrap` (Orchestrateur Principal)

**Bibind** est une plateforme d’orchestration IA pour la création, le déploiement et la gestion de solutions SaaS sur des infrastructures cloud modulaires.  
Ce service FastAPI, appelé `op_bootstrap`, joue le rôle d’orchestrateur principal, pilotant l’ensemble des sous-orchestrateurs (SO) via Kafka, LangGraph, Flyte, et des modèles LLM comme Ollama/OpenAI.

---

## 🧠 Rôle de `op_bootstrap`

- Gérer les utilisateurs, organisations et projets
- Analyser les prompts utilisateur via LLM
- Proposer des **offres SaaS standards** du catalogue ou lancer un **workflow IA de création personnalisée**
- Déclencher les SOs via événements Kafka
- Piloter des workflows dynamiques avec LangGraph
- Lancer des exécutions de pipelines avec Flyte
- Suivre l’avancement des tâches pour intégration Odoo
- Générer des inventaires Ansible à partir de `tfstate`

---

## 🚀 Fonctionnalités principales

| Module | Description |
|--------|-------------|
| 🔐 Auth | Intégration OAuth2 / Keycloak |
| 🧾 Catalogue | Gestion des types d’offres et d’infrastructures |
| 🧱 Infrastructure | Génération d’inventaire, suivi, monitoring |
| 📦 Offre SaaS | Création, déploiement, rattachement à projet |
| 🧩 LangGraph | Routage intelligent des workflows IA |
| ⚙️ Flyte | Déploiement asynchrone d’offres ou tests |
| 📣 Kafka | Communication inter-SO via topics organisés |
| 📁 GitLab / Vault / MinIO | Intégration CI/CD et persistance |
| 🧑‍💻 Odoo | Interface utilisateur pour pilotage et facturation |

---

## 🗂️ Arborescence clé

```
op_bootstrap/
├── app/
│   ├── routes/          # Routes API pour les entités métier et orchestrateurs
│   ├── models/          # Modèles SQLAlchemy (persistants)
│   ├── schemas/         # Schémas Pydantic (validation)
│   ├── services/        # Logique métier (décision IA, flyte launcher, etc.)
│   ├── langgraph/       # Workflows et noeuds LangGraph
│   ├── flyte/           # Déploiements Flyte
│   ├── clients/         # API externes (Vault, GitLab, MinIO, etc.)
│   ├── utils/           # Kafka, loggers, générateurs d’événements
│   ├── crud/            # Accès DB
│   └── tests/           # Tests unitaires et fonctionnels
```

---

## ⚙️ Installation

### Prérequis

- Docker / Docker Compose
- Python 3.10+
- Kafka (ex : Bitnami en Helm chart)
- PostgreSQL
- Keycloak, GitLab, Vault, MinIO, Flyte (local ou sur cluster K8s)

### Lancer en local (développement)

```bash
# 1. Créer l'environnement
python3 -m venv venv
source venv/bin/activate

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Lancer l'app localement
uvicorn app.main:app --reload
```

### Via Docker Compose

```bash
docker compose up --build
```

---

## 📡 API & Documentation

- Swagger UI : http://localhost:8000/docs
- Redoc : http://localhost:8000/redoc
- Auth : OAuth2 avec Keycloak
- Communication SO : Kafka topics configurés via `so_mapping.yaml`

---

## 📬 Kafka Topics Exemple

| Topic                    | Description                                 |
|--------------------------|---------------------------------------------|
| `so_conception.tasks`    | Déclenchement d’analyse conceptuelle        |
| `so_qualite.tasks`       | Analyse des livrables générés               |
| `so_release.deployment`  | Validation et déploiement final             |

---

## 📁 Inventaires Ansible

Générés à partir des fichiers `.tfstate` post-déploiement Flyte.

- Fichier : `infrastructure_inventory.json`
- Utilisés dans AWX pour automatiser les playbooks

---

## 🧪 Tests

```bash
pytest tests/
```

---

## 🧠 LangChain / LangGraph

- LangGraph : orchestration dynamique des actions IA
- Ollama / OpenAI : modèles pour prompt engineering et analyse
- Flyte : tâches longues et déploiements asynchrones

---

## 🧩 SOs intégrés

- `so_conception`
- `so_organisation`
- `so_planification`
- `so_realisation`
- `so_qualite`
- `so_release`

Chaque SO est une API FastAPI dédiée, autonome, et abonnée à Kafka.

---

## 👥 Utilisateurs et Rôles

- Utilisateur simple : souscrit à une offre existante
- Expert : crée des offres personnalisées
- Admin : développe de nouveaux types d’infrastructure/offres
- Chaque action IA ou SO est journalisée avec un `event_id`

---

## 🧾 Licence

Bibind est un projet sous licence MIT. Pour tout usage commercial, veuillez nous contacter.

---

## 🤝 Contribuer

Les contributions sont les bienvenues !  
Clonez le repo, créez une branche `feature/`, ajoutez vos modifications et soumettez un MR.

---

## 📬 Contact

- Site : [bibind.local](http://bibind.local)
- Odoo Front : [odoo.bibind.local](http://odoo.bibind.local)
- Email : contact@bibind.io