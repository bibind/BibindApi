"""CRUD operations for MachineDefinition."""

from app.models.machine_definition import MachineDefinition
from .base import CRUDBase

crud_machine_definition = CRUDBase(MachineDefinition)

get = crud_machine_definition.get
get_multi = crud_machine_definition.get_multi
create = crud_machine_definition.create
