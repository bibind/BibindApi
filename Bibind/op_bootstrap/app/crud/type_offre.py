"""CRUD operations for TypeOffre."""

from app.models.type_offre import TypeOffre
from .base import CRUDBase

crud_type_offre = CRUDBase(TypeOffre)

get = crud_type_offre.get
get_multi = crud_type_offre.get_multi
create = crud_type_offre.create
