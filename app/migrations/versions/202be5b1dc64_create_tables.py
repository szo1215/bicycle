"""create tables

Revision ID: 202be5b1dc64
Revises: 
Create Date: 2015-09-28 21:46:17.779272

"""

# revision identifiers, used by Alembic.
revision = '202be5b1dc64'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('user',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(length=255), nullable=True),
                    sa.Column('name', sa.String(length=255), nullable=True),
                    sa.Column('password', sa.String(length=255), 
                              nullable=True),
                    sa.Column('created_date', sa.DateTime(timezone=True), 
                              nullable=False),
                    sa.PrimaryKeyConstraint('id'))
    op.create_index(op.f('ix_user_created_date'), 'user', ['created_date'], 
                    unique=False)
    op.create_table('riding',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=True),
                    sa.Column('title', sa.String(length=255), nullable=True),
                    sa.Column('created_date', sa.DateTime(timezone=True), 
                              nullable=False),
                    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
                    sa.PrimaryKeyConstraint('id'))
    op.create_index(op.f('ix_riding_created_date'), 'riding', ['created_date'], 
                    unique=False)
    op.create_table('gps',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('riding_id', sa.Integer(), nullable=True),
                    sa.Column('latitude', sa.Float(), nullable=True),
                    sa.Column('longtitude', sa.Float(), nullable=True),
                    sa.Column('altitude', sa.Float(), nullable=True),
                    sa.Column('horizontal_accuracy', sa.Float(), 
                              nullable=True),
                    sa.Column('vertical_accuracy', sa.Float(), nullable=True),
                    sa.Column('timestamp', sa.DateTime(timezone=True), 
                              nullable=False),
                    sa.ForeignKeyConstraint(['riding_id'], ['riding.id'], ),
                    sa.PrimaryKeyConstraint('id'))
    op.create_index(op.f('ix_gps_timestamp'), 'gps', ['timestamp'], 
                    unique=False)

def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_gps_timestamp'), table_name='gps')
    op.drop_table('gps')
    op.drop_index(op.f('ix_riding_created_date'), table_name='riding')
    op.drop_table('riding')
    op.drop_index(op.f('ix_user_created_date'), table_name='user')
    op.drop_table('user')
    ### end Alembic commands ###
