"""CRUD operations for Offre."""

from app.models.offre import Offre
from .base import CRUDBase

crud_offre = CRUDBase(Offre)

get = crud_offre.get
get_multi = crud_offre.get_multi
create = crud_offre.create
