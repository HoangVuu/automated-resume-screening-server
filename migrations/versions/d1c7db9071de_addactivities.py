"""addActivities

Revision ID: d1c7db9071de
Revises: bd7dd4a9b6e6
Create Date: 2020-12-19 22:40:36.777982

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd1c7db9071de'
down_revision = 'bd7dd4a9b6e6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('activity_parameters',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('activity_types',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.String(length=200), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('activities',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('activity_type_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['activity_type_id'], ['activity_types.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('activity_details',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('activity_id', sa.Integer(), nullable=False),
    sa.Column('activity_parameter_id', sa.Integer(), nullable=False),
    sa.Column('value', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['activity_id'], ['activities.id'], ),
    sa.ForeignKeyConstraint(['activity_parameter_id'], ['activity_parameters.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('activity_details')
    op.drop_table('activities')
    op.drop_table('activity_types')
    op.drop_table('activity_parameters')
    # ### end Alembic commands ###