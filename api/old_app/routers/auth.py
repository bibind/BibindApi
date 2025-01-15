from fastapi import APIRouter, HTTPException, Depends
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from pydantic import BaseModel
from app.db.database import get_db
from typing import Optional

# Configurations pour JWT
SECRET_KEY = "your_secret_key_here_please_use_env_variables"  # Utilise settings.SECRET_KEY en production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes de validité du token

# Contexte pour le hachage des mots de passe
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Modèles Pydantic pour les requêtes
class User(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


# Une fausse base de données pour le test local
fake_users_db = {}


# Vérification du hashage de mots de passe
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password):
    return pwd_context.hash(password)


# Génération d'un token d'accès
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)  # Par défaut 15 min
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Vérification du token
def get_current_user(token: str = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token invalide")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Token invalide ou expiré")


# Création du routeur
router = APIRouter()


@router.post("/register", response_model=Token)
def register(user: User):
    # Vérifie si le nom d'utilisateur existe déjà
    if user.username in fake_users_db:
        raise HTTPException(status_code=400, detail="Utilisateur déjà enregistré")

    # Hacher le mot de passe et stocker l'utilisateur dans la "DB"
    hashed_password = hash_password(user.password)
    fake_users_db[user.username] = {"username": user.username, "hashed_password": hashed_password}

    # Création du token JWT
    access_token = create_access_token(data={"sub": user.username},
                                       expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login", response_model=Token)
def login(user: User):
    db_user = fake_users_db.get(user.username)
    if not db_user or not verify_password(user.password, db_user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Identifiants invalides")

    # Création du token JWT
    access_token = create_access_token(data={"sub": user.username},
                                       expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me")
def get_me(current_user: str = Depends(get_current_user)):
    return {"username": current_user}# Gestion JWT/OAuth2
