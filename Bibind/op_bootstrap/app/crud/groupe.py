"""CRUD operations for Groupe."""

from app.models.groupe import Groupe
from .base import CRUDBase

crud_groupe = CRUDBase(Groupe)

get = crud_groupe.get
get_multi = crud_groupe.get_multi
create = crud_groupe.create
