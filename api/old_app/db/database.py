from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

#DATABASE_URL = f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.POSTGRES_DB}"
DATABASE_URL = settings.DATABASE_URL
# Création du moteur SQLAlchemy
engine = create_async_engine(DATABASE_URL, echo=True)

# Session asynchrone
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


# Middleware pour les sessions de base de données
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


# Méthodes de démarrage et de fermeture
async def init_db():
    async with engine.begin() as conn:
        # Vérifie la connexion, ajoute des migrations ou autres initialisations
        await conn.run_sync(Base.metadata.create_all)


async def close_db():
    await engine.dispose()