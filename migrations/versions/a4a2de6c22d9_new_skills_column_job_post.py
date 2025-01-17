"""new_skills_column_job_post

Revision ID: a4a2de6c22d9
Revises: 2a68a76b811a
Create Date: 2021-01-25 19:49:10.676087

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'a4a2de6c22d9'
down_revision = '367f598a64bf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('job_posts', sa.Column('general_skills', sa.Text(), nullable=False))
    op.alter_column('job_posts', 'soft_skills',
               existing_type=mysql.VARCHAR(length=500),
               type_=mysql.TEXT(collation='utf8_unicode_ci'),
               nullable=False)
    op.drop_column('job_posts', 'technical_skills')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('job_posts', sa.Column('technical_skills', mysql.VARCHAR(length=500), nullable=True))
    op.alter_column('job_posts', 'soft_skills',
               existing_type=mysql.TEXT(collation='utf8_unicode_ci'),
               type_=mysql.VARCHAR(length=500),
               nullable=True)
    op.drop_column('job_posts', 'general_skills')
    # ### end Alembic commands ###
