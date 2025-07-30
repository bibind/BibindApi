FROM python:3.11-slim

# Dépendances système
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc curl git build-essential libssl-dev && \
    rm -rf /var/lib/apt/lists/*

# Création des dossiers applicatifs
WORKDIR /app

# Ajout des fichiers de dépendances
COPY requirements.txt .

# Installation des dépendances Python
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copie du code
COPY . .

# Port par défaut
EXPOSE 8000

# Lancement de FastAPI via Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
