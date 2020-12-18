"""removeRemote

Revision ID: 1fda627944ff
Revises: 6db8da2c90b6
Create Date: 2020-12-18 19:34:06.609352

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '1fda627944ff'
down_revision = '6db8da2c90b6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('job_post_detail', 'allow_remote')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('job_post_detail', sa.Column('allow_remote', mysql.TINYINT(display_width=1), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
