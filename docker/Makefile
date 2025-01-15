# =====================================
# Variables et Fichiers Communes
# =====================================
DOCKER_COMPOSE=docker-compose
DOCKER_COMPOSE_FILES=$(DOCKER_COMPOSE).api.yml $(DOCKER_COMPOSE).hydra-kratos.yml $(DOCKER_COMPOSE).odoo.yml $(DOCKER_COMPOSE).gitlab.yml $(DOCKER_COMPOSE).awx.yml
mkfile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
current_dir := $(notdir $(patsubst %/,%,$(dir $(mkfile_path))))
cur_dir=${shell pwd}
parent_dir=${shell dirname ${shell pwd}}
# Variables génériques d'environnement
BACKEND_IMAGE=bindingapi-backend
FRONTEND_IMAGE=bindingapi-frontend

.PHONY: up-api up-hydra-kratos up-odoo up-awx up-gitlab up-all \
        down-api down-hydra-kratos down-odoo down-awx down-gitlab down-all \
        build-api build-hydra-kratos build-odoo build-awx build-gitlab build-all \
        start-api-hydra restart-api test backend-shell help clean

# =====================================
# 1. Lancement/Arrêt des Services
# =====================================

# Lancer BibindAPI seul
up-api:
	@echo "🚀 Lancement de BibindAPI (backend + database)..."
	docker-compose -f $(DOCKER_COMPOSE).api.yml up -d

# Lancer Hydra + Kratos
up-hydra-kratos:
	@echo "🚀 Lancement de Hydra et Kratos (authentification)..."
	docker-compose -f $(DOCKER_COMPOSE).hydra-kratos.yml up -d

# Lancer Odoo
up-odoo:
	@echo "🚀 Lancement de Odoo..."
	docker-compose -f $(DOCKER_COMPOSE).odoo.yml up -d

# Lancer GitLab
up-gitlab:
	@echo "🚀 Lancement de GitLab..."
	docker-compose -f $(DOCKER_COMPOSE).gitlab.yml up -d

# Lancer AWX
up-awx:
	@echo "🚀 Lancement de AWX..."
	docker-compose -f $(DOCKER_COMPOSE).awx.yml up -d

# Lancer tous les services
up-all: up-api up-hydra-kratos up-odoo up-gitlab up-awx
	@echo "🚀 Tous les services sont démarrés."

# Arrêter BibindAPI
down-api:
	@echo "🛑 Arrêt de BibindAPI..."
	docker-compose -f $(DOCKER_COMPOSE).api.yml down

# Arrêter Hydra + Kratos
down-hydra-kratos:
	@echo "🛑 Arrêt de Hydra et Kratos..."
	docker-compose -f $(DOCKER_COMPOSE).hydra-kratos.yml down

# Arrêter Odoo
down-odoo:
	@echo "🛑 Arrêt de Odoo..."
	docker-compose -f $(DOCKER_COMPOSE).odoo.yml down

# Arrêter GitLab
down-gitlab:
	@echo "🛑 Arrêt de GitLab..."
	docker-compose -f $(DOCKER_COMPOSE).gitlab.yml down

# Arrêter AWX
down-awx:
	@echo "🛑 Arrêt de AWX..."
	docker-compose -f $(DOCKER_COMPOSE).awx.yml down

# Arrêter tous les services
down-all: down-api down-hydra-kratos down-odoo down-gitlab down-awx
	@echo "🛑 Tous les services sont arrêtés."

# Redémarrer BibindAPI et Hydra/Kratos pour les tests d'authentification
restart-api:
	@echo "🔄 Redémarrage de BibindAPI et Hydra/Kratos..."
	$(MAKE) down-api down-hydra-kratos
	$(MAKE) up-api up-hydra-kratos

# =====================================
# 2. Build des Services Docker
# =====================================

# Construire l'image Docker pour BibindAPI
build-api:
	@echo "🔨 Construction des images pour BibindAPI..."
	docker-compose -f $(DOCKER_COMPOSE).api.yml --env-file $(parent_dir)/api/.env build

# Construire Hydra et Kratos
build-hydra-kratos:
	@echo "🔨 Construction des images pour Hydra et Kratos..."
	docker-compose -f $(DOCKER_COMPOSE).hydra-kratos.yml build

# Construire Odoo
build-odoo:
	@echo "🔨 Construction de l'image Odoo..."
	docker-compose -f $(DOCKER_COMPOSE).odoo.yml build

# Construire GitLab
build-gitlab:
	@echo "🔨 Construction des images GitLab..."
	docker-compose -f $(DOCKER_COMPOSE).gitlab.yml build

# Construire AWX
build-awx:
	@echo "🔨 Construction des images AWX..."
	docker-compose -f $(DOCKER_COMPOSE).awx.yml build

# Construire toutes les images Docker
build-all: build-api build-hydra-kratos build-odoo build-gitlab build-awx
	@echo "✅ Toutes les images Docker ont été construites avec succès."

# =====================================
# 3. Tests et Debug
# =====================================

# Exécuter les tests unitaires sur BibindAPI
test:
	@echo "⚙️ Exécution des tests unitaires sur BibindAPI..."
	docker-compose -f $(DOCKER_COMPOSE).api.yml run --rm api pytest tests/

# Shell dans le conteneur backend pour debug
backend-shell:
	@echo "💻 Connexion au conteneur backend pour debug..."
	docker exec -it $(BACKEND_IMAGE) /bin/sh || { echo "❌ Impossible d'ouvrir une session dans le conteneur backend."; exit 1; }

# =====================================
# 4. Nettoyage
# =====================================

clean: down-all
	@echo "🧹 Suppression des volumes Docker persistants..."
	docker volume prune -f

# =====================================
# 5. Aide
# =====================================

help:
	@echo "📜 Liste des commandes Makefile disponibles :"
	@echo ""
	@echo "Lancement des services :"
	@echo "  up-api               - Lance BibindAPI (backend + database)."
	@echo "  up-hydra-kratos      - Lance Hydra et Kratos."
	@echo "  up-odoo              - Lance Odoo."
	@echo "  up-gitlab            - Lance GitLab."
	@echo "  up-awx               - Lance AWX."
	@echo "  up-all               - Lance tous les services."
	@echo ""
	@echo "Arrêt des services :"
	@echo "  down-api             - Arrête BibindAPI."
	@echo "  down-hydra-kratos    - Arrête Hydra et Kratos."
	@echo "  down-odoo            - Arrête Odoo."
	@echo "  down-gitlab          - Arrête GitLab."
	@echo "  down-awx             - Arrête AWX."
	@echo "  down-all             - Arrête tous les services."
	@echo ""
	@echo "Build des services :"
	@echo "  build-api            - Construit les images pour BibindAPI."
	@echo "  build-hydra-kratos   - Construit les images pour Hydra/Kratos."
	@echo "  build-odoo           - Construit les images pour Odoo."
	@echo "  build-gitlab         - Construit les images pour GitLab."
	@echo "  build-awx            - Construit les images pour AWX."
	@echo "  build-all            - Construit toutes les images."
	@echo ""
	@echo "Autres :"
	@echo "  restart-api          - Redémarre BibindAPI et Hydra/Kratos."
	@echo "  clean                - Supprime tous les volumes persistants."
	@echo "  backend-shell        - Ouvre une session shell dans le conteneur backend."
	@echo "  test                 - Exécute les tests unitaires sur BibindAPI."
	@echo "  help                 - Affiche cette aide."