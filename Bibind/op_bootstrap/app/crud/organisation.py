"""CRUD operations for Organisation."""

from app.models.organisation import Organisation
from .base import CRUDBase

crud_organisation = CRUDBase(Organisation)

get = crud_organisation.get
get_multi = crud_organisation.get_multi
create = crud_organisation.create
