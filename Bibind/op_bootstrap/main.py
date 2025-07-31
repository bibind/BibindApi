from fastapi import FastAPI

from app.routes import auth, users, organisations, groupes, files
from app.routes.catalogues import type_infrastructure, type_offre
from app.routes.infrastructures import infrastructure, inventory, monitoring
from app.routes.offres import offre, solution, projet
from app.routes.orchestrateur import principal, trigger, events, langgraph
from app.routes.validation import human_validation

app = FastAPI(title="Operational Bootstrap")

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(organisations.router)
app.include_router(groupes.router)
app.include_router(type_infrastructure.router)
app.include_router(type_offre.router)
app.include_router(infrastructure.router)
app.include_router(inventory.router)
app.include_router(monitoring.router)
app.include_router(offre.router)
app.include_router(solution.router)
app.include_router(projet.router)
app.include_router(files.router)
app.include_router(principal.router)
app.include_router(trigger.router)
app.include_router(events.router)
app.include_router(langgraph.router)
app.include_router(human_validation.router)


@app.get("/health")
async def health() -> dict:
    """Simple health check endpoint."""
    return {"status": "ok"}
