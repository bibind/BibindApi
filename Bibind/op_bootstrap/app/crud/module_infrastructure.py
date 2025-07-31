"""CRUD operations for ModuleInfrastructure."""

from app.models.module_infrastructure import ModuleInfrastructure
from .base import CRUDBase

crud_module_infrastructure = CRUDBase(ModuleInfrastructure)

get = crud_module_infrastructure.get
get_multi = crud_module_infrastructure.get_multi
create = crud_module_infrastructure.create
