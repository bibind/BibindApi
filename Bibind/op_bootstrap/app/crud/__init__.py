from .base import CRUDBase
from app.models import (
    User,
    Organisation,
    Projet,
    Offre,
    Groupe,
    Infrastructure,
    Inventory,
    MachineDefinition,
    ModuleInfrastructure,
    Solution,
    TypeInfrastructure,
    TypeOffre,
)

user = CRUDBase(User)
organisation = CRUDBase(Organisation)
projet = CRUDBase(Projet)
offre = CRUDBase(Offre)
groupe = CRUDBase(Groupe)
infrastructure = CRUDBase(Infrastructure)
inventory = CRUDBase(Inventory)
machine_definition = CRUDBase(MachineDefinition)
module_infrastructure = CRUDBase(ModuleInfrastructure)
solution = CRUDBase(Solution)
type_infrastructure = CRUDBase(TypeInfrastructure)
type_offre = CRUDBase(TypeOffre)

__all__ = [
    "user",
    "organisation",
    "projet",
    "offre",
    "groupe",
    "infrastructure",
    "inventory",
    "machine_definition",
    "module_infrastructure",
    "solution",
    "type_infrastructure",
    "type_offre",
]
