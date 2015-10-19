"""edit column name

Revision ID: 418ee445bf23
Revises: 202be5b1dc64
Create Date: 2015-10-19 13:12:15.549993

"""

# revision identifiers, used by Alembic.
revision = '418ee445bf23'
down_revision = '202be5b1dc64'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    op.add_column('gps', sa.Column('longitude', sa.Float(), nullable=True))
    op.drop_column('gps', 'longtitude')


def downgrade():
    op.add_column('gps', sa.Column('longtitude', 
                    postgresql.DOUBLE_PRECISION(precision=53), 
                                                autoincrement=False, 
                                                nullable=True))
    op.drop_column('gps', 'longitude')

