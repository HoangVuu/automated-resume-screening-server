"""updateResume

Revision ID: 367f598a64bf
Revises: 4ab9938291c2
Create Date: 2021-01-18 23:57:14.884651

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '367f598a64bf'
down_revision = '4ab9938291c2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('resumes', sa.Column('created_on', sa.DateTime(), nullable=True))
    op.add_column('resumes', sa.Column('last_edit', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('resumes', 'last_edit')
    op.drop_column('resumes', 'created_on')
    # ### end Alembic commands ###
