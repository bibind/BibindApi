"""CRUD operations for Solution."""

from app.models.solution import Solution
from .base import CRUDBase

crud_solution = CRUDBase(Solution)

get = crud_solution.get
get_multi = crud_solution.get_multi
create = crud_solution.create
