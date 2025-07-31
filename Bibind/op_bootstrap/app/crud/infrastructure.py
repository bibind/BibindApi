"""CRUD operations for Infrastructure."""

from app.models.infrastructure import Infrastructure
from .base import CRUDBase

crud_infrastructure = CRUDBase(Infrastructure)

get = crud_infrastructure.get
get_multi = crud_infrastructure.get_multi
create = crud_infrastructure.create
