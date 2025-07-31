"""CRUD operations for Projet."""

from app.models.projet import Projet
from .base import CRUDBase

crud_projet = CRUDBase(Projet)

get = crud_projet.get
get_multi = crud_projet.get_multi
create = crud_projet.create
