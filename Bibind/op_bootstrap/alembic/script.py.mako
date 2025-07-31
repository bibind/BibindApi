<%text>#
# This file is part of Alembic.
# It is provided here for convenience, mostly to generate migration
# scripts via `alembic revision --autogenerate`.
#</%text>

from alembic import op
import sqlalchemy as sa

${imports if imports else ""}

def upgrade():
${upgrades if upgrades else "    pass"}

def downgrade():
${downgrades if downgrades else "    pass"}
