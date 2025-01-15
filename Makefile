# Variables d'environnement
BACKEND_IMAGE=bindingapi-backend
FRONTEND_IMAGE=bindingapi-frontend
DOCKER_REGISTRY=your_private_registry
KUBECTL=kubectl
CHARMS_PATH=charms/
DOCKER_COMPOSE_FILE=docker/docker-compose.yml
BUILD_CONTEXT=.

.PHONY: build-backend build-frontend build build-all up down clean restart test test-backend backend-shell docker-check docker-install check-permissions deploy-charm deploy-charm-all check-requirements help

####################
# Vérifications globales
####################

# Vérifie si l'utilisateur est root
check-root:
	@if [ "$$(id -u)" -eq 0 ]; then \
		echo "❌ Ne pas exécuter \`make\` en tant que root. Relancez avec un utilisateur standard."; \
		exit 1; \
	fi

# Vérifie si Docker et Docker Compose sont installés, et si l'utilisateur dispose des permissions
docker-check: check-root
	@echo "✅ Vérification de Docker et Docker Compose..."
	@if ! [ -x "$$(command -v docker)" ]; then \
		echo "❌ Docker n'est pas installé."; \
		echo "👉 Installez Docker en exécutant \`make docker-install\`."; \
		exit 1; \
	fi
	@if ! [ -x "$$(command -v docker-compose)" ]; then \
		echo "❌ Docker Compose n'est pas installé."; \
		echo "👉 Lancez \`make docker-install\` pour l'installer automatiquement."; \
		exit 1; \
	fi
	@if ! [ -w /var/run/docker.sock ]; then \
		echo "❌ L'utilisateur actuel n'a pas les permissions pour utiliser Docker."; \
		echo "👉 Exécutez la commande suivante pour corriger : \`sudo usermod -aG docker $$USER\`."; \
		exit 1; \
	fi
	@echo "✅ Docker et Docker Compose sont disponibles, et permissions OK."

# Installe Docker et Docker Compose sous Ubuntu 22.04
docker-install: check-root
	@echo "🔄 Installation de Docker et Docker Compose pour Ubuntu 22.04..."
	@sudo apt-get update
	@sudo apt-get install -y \
		ca-certificates \
		curl \
		gnupg \
		lsb-release
	@sudo mkdir -p /etc/apt/keyrings
	@curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
	@echo \
		"deb [arch=$$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
		$$(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
	@sudo apt-get update
	@sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
	@echo "✅ Docker et Docker Compose installés avec succès."

# Vérifie les permissions Docker avant de lancer une commande nécessitant Docker
check-permissions: docker-check
	@if ! docker info > /dev/null 2>&1; then \
		echo "❌ Impossible d'exécuter Docker. Vérifiez les permissions utilisateur."; \
		exit 1; \
	fi

####################
# Gestion des images Docker
####################

# Construire l'image Backend avec le bon contexte
build-backend: check-permissions
	@echo "🔨 Construction de l'image Docker Backend..."
	@if [ -f api/Dockerfile-backend ]; then \
		docker build -t $(BACKEND_IMAGE) -f api/Dockerfile-backend ./api || { echo "❌ Échec de la construction de l'image backend."; exit 1; }; \
	else \
	    echo "❌ Le fichier api/Dockerfile-backend est introuvable."; \
	    exit 1; \
	fi
	@echo "✅ Image Backend construite avec succès."

# Construire l'image Frontend avec le bon contexte
build-frontend: check-permissions
	@echo "🔨 Construction de l'image Docker Frontend..."
	@if [ -f frontend/Dockerfile-frontend ]; then \
		docker build -t $(FRONTEND_IMAGE) -f frontend/Dockerfile-frontend ./frontend || { echo "❌ Échec de la construction de l'image frontend."; exit 1; }; \
	else \
	    echo "❌ Le fichier frontend/Dockerfile-frontend est introuvable."; \
	    exit 1; \
	fi
	@echo "✅ Image Frontend construite avec succès."

# Construire toutes les images (backend et frontend)
build-all: build-backend build-frontend

# Construire les images via Docker Compose
build: check-permissions
	@echo "🔨 Construction des services via docker-compose..."
	@if [ ! -f $(DOCKER_COMPOSE_FILE) ]; then \
		echo "❌ Le fichier $(DOCKER_COMPOSE_FILE) est introuvable."; \
		exit 1; \
	fi
	docker-compose -f $(DOCKER_COMPOSE_FILE) build || { echo "❌ Échec de la construction des services Docker via Compose."; exit 1; }
	@echo "✅ Services construits avec succès via Compose."

####################
# Gestion des services Docker Compose
####################

# Lancer les services
up: build
	@echo "🚀 Lancement des services avec Docker Compose..."
	docker-compose -f $(DOCKER_COMPOSE_FILE) up -d || { echo "❌ Échec du démarrage des services."; exit 1; }

# Arrêter les conteneurs Docker
down: check-permissions
	@echo "🛑 Arrêt des services Docker Compose..."
	docker-compose -f $(DOCKER_COMPOSE_FILE) down || { echo "❌ Échec de l'arrêt des services."; exit 1; }

# Nettoyer les volumes persistants
clean: down
	@echo "🧹 Suppression des volumes persistants..."
	docker volume rm bindingapi_postgres_data || true
	@echo "✅ Nettoyage terminé."

# Redémarrer les services (arrêt + démarrage)
restart: down up
	@echo "🔄 Services redémarrés avec succès."

####################
# Tests et Debug
####################

# Vérifier les dépendances dans requirements.txt via un fichier Dockerfile spécifique
check-requirements: check-permissions
	@echo "📦 Vérification des dépendances dans api/requirements.txt..."
	@if [ ! -f api/requirements.txt ]; then \
		echo "❌ Fichier api/requirements.txt introuvable."; \
		exit 1; \
	fi
	@docker build --no-cache -t verify-requirements -f api/Dockerfile-backend ./api || { echo "❌ Échec de la vérification des dépendances."; exit 1; }
	@docker run --rm verify-requirements || { echo "❌ Erreur dans requirements.txt ou dépendances manquantes."; exit 1; }
	@echo "✅ Toutes les dépendances dans api/requirements.txt sont valides."

# Exécuter les tests unitaires avec pytest dans le conteneur backend
test: check-permissions
	@echo "🧪 Exécution des tests unitaires (backend)..."
	@if docker-compose ps | grep -q $(BACKEND_IMAGE); then \
		docker exec -it $(BACKEND_IMAGE) pytest tests/ || { echo "❌ Échec des tests."; exit 1; }; \
	else \
		echo "❌ Aucun conteneur backend actif pour exécuter les tests."; \
	fi

# Se connecter au conteneur backend pour effectuer un debug
backend-shell: check-permissions
	@echo "💻 Connexion au conteneur backend..."
	docker exec -it $(BACKEND_IMAGE) /bin/sh || { echo "❌ Impossible d'ouvrir une session dans le conteneur backend."; exit 1; }

####################
# Gestion des charms Juju
####################

# Pack et déploie un charm spécifique
deploy-charm: check-permissions
	@cd $(CHARMS_PATH)BibindApi/ && charmcraft pack && juju deploy $(CHARMS_PATH)BibindApi/bibindapi.charm --trust || { echo "❌ Échec du déploiement du charm BibindApi."; exit 1; }

# Pack et déploie tous les charms présents dans le dossier `charms/`
deploy-charm-all: check-permissions
	@for CHARM in $(CHARMS_PATH)*; do \
		(cd $$CHARM && charmcraft pack); \
		juju deploy $$CHARM/*.charm --trust || { echo "❌ Échec du déploiement d'un charm dans $$CHARM."; exit 1; }; \
	done
	@echo "✅ Tous les charms ont été packés et déployés avec succès."

####################
# Aide
####################

# Affiche l'aide
help:
	@echo "📜 Commandes disponibles dans ce Makefile :"
	@echo ""
	@echo "🔧 Docker Setup :"
	@echo "  docker-check       - Vérifie si Docker et Docker Compose sont bien configurés."
	@echo "  docker-install     - Installe Docker et Docker Compose sous Ubuntu 22.04."
	@echo "  check-permissions  - Vérifie les permissions de l'utilisateur pour Docker."
	@echo ""
	@echo "🔍 Build :"
	@echo "  build-backend      - Construit l'image Docker du backend."
	@echo "  build-frontend     - Construit l'image Docker du frontend."
	@echo "  build-all          - Construit entièrement les images backend et frontend."
	@echo "  build              - Construit les services Docker à l'aide de Docker Compose."
	@echo ""
	@echo "🚀 Gestion des Services :"
	@echo "  up                 - Déploie les services Docker Compose."
	@echo "  down               - Arrête les services et conteneurs."
	@echo "  clean              - Nettoie les volumes."
	@echo "  restart            - Redémarre les services."
	@echo ""
	@echo "🧪 Tests et Debug :"
	@echo "  check-requirements - Vérifie les dépendances dans api/requirements.txt."
	@echo "  test               - Exécute les tests unitaires backend."
	@echo "  backend-shell      - Ouvre un shell dans le conteneur backend pour debug."
	@echo ""
	@echo "🎛 Gestion des Charms :"
	@echo "  deploy-charm       - Pack et déploie un charm via Juju."
	@echo "  deploy-charm-all   - Déploie tous les charms présents dans \`charms/\`."
	@echo ""
	@echo "⚡ Utilisez \`make <commande>\` pour exécuter une commande."