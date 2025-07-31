"""CRUD operations for TypeInfrastructure."""

from app.models.type_infrastructure import TypeInfrastructure
from .base import CRUDBase

crud_type_infrastructure = CRUDBase(TypeInfrastructure)

get = crud_type_infrastructure.get
get_multi = crud_type_infrastructure.get_multi
create = crud_type_infrastructure.create
