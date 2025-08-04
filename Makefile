.PHONY: check-docker install-docker setup all

check-docker:
	@echo "Vérification de l'installation de Docker..."
	@if command -v docker >/dev/null 2>&1; then \
		echo "Docker est installé."; \
	else \
		echo "Docker n'est pas installé."; \
		exit 1; \
	fi

install-docker:
	@if ! command -v docker >/dev/null 2>&1; then \
		echo "Installation de Docker..."; \
		curl -fsSL https://get.docker.com -o get-docker.sh && sh get-docker.sh; \
		rm -f get-docker.sh; \
	else \
		echo "Docker est déjà installé."; \
	fi

setup: install-docker
	@echo "Lancement des scripts de configuration..."
	@if [ -f ./setup.sh ]; then \
		echo "Exécution de ./setup.sh"; \
		bash ./setup.sh; \
	else \
		echo "Aucun script setup.sh trouvé."; \
	fi

all: setup
	@echo "Configuration complète."
