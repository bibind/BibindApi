"""CRUD operations for User."""

from sqlalchemy.orm import Session

from app.models.user import User
from .base import CRUDBase

crud_user = CRUDBase(User)

get = crud_user.get
get_multi = crud_user.get_multi
create = crud_user.create
