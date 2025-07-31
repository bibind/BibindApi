"""Initial tables"""
from alembic import op
import sqlalchemy as sa

revision = '0001_initial'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'organisations',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(), nullable=False, unique=True),
    )
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('email', sa.String(), nullable=False, unique=True),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='1'),
        sa.Column('organisation_id', sa.Integer, sa.ForeignKey('organisations.id')),
    )
    op.create_table(
        'projets',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('organisation_id', sa.Integer, sa.ForeignKey('organisations.id')),
    )
    op.create_table(
        'offres',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.String()),
        sa.Column('projet_id', sa.Integer, sa.ForeignKey('projets.id')),
    )
    op.create_table(
        'groupes',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
    )
    op.create_table(
        'infrastructures',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
    )
    op.create_table(
        'inventories',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
    )
    op.create_table(
        'machine_definitions',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
    )
    op.create_table(
        'modules_infrastructure',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
    )
    op.create_table(
        'solutions',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
    )
    op.create_table(
        'types_infrastructure',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
    )
    op.create_table(
        'types_offre',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
    )

def downgrade():
    op.drop_table('types_offre')
    op.drop_table('types_infrastructure')
    op.drop_table('solutions')
    op.drop_table('modules_infrastructure')
    op.drop_table('machine_definitions')
    op.drop_table('inventories')
    op.drop_table('infrastructures')
    op.drop_table('groupes')
    op.drop_table('offres')
    op.drop_table('projets')
    op.drop_table('users')
    op.drop_table('organisations')
