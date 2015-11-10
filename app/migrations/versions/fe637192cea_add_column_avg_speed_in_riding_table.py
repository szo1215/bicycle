"""add column avg_speed in Riding table

Revision ID: fe637192cea
Revises: 476d3248c80f
Create Date: 2015-11-10 16:16:57.310657

"""

# revision identifiers, used by Alembic.
revision = 'fe637192cea'
down_revision = '476d3248c80f'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('riding', sa.Column('avg_speed', sa.Float(), nullable=True))


def downgrade():
    op.drop_column('riding', 'avg_speed')

