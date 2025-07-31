"""CRUD operations for Inventory."""

from app.models.inventory import Inventory
from .base import CRUDBase

crud_inventory = CRUDBase(Inventory)

get = crud_inventory.get
get_multi = crud_inventory.get_multi
create = crud_inventory.create
