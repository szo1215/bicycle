"""create table riding_rank

Revision ID: 476d3248c80f
Revises: 418ee445bf23
Create Date: 2015-10-20 14:24:59.976030

"""

# revision identifiers, used by Alembic.
revision = '476d3248c80f'
down_revision = '418ee445bf23'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('riding_rank',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('created_date', sa.DateTime(timezone=True), 
                              nullable=False),
                    sa.Column('riding_id', sa.Integer(), nullable=True),
                    sa.Column('avg_speed', sa.Float(), nullable=True),
                    sa.ForeignKeyConstraint(['riding_id'], ['riding.id'], ),
                    sa.PrimaryKeyConstraint('id'))
    op.create_index(op.f('ix_riding_rank_created_date'), 
                         'riding_rank', ['created_date'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_riding_rank_created_date'), 
                       table_name='riding_rank')
    op.drop_table('riding_rank')

