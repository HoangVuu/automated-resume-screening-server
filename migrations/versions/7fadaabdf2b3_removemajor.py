"""removeMajor

Revision ID: 7fadaabdf2b3
Revises: daf0da8c54c9
Create Date: 2021-01-05 19:43:09.274702

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '7fadaabdf2b3'
down_revision = 'daf0da8c54c9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('candidate_education', sa.Column('degree_level', sa.Integer(), nullable=False))
    op.add_column('candidate_education', sa.Column('major', sa.String(length=255), nullable=False))
    op.drop_constraint('candidate_education_ibfk_1', 'candidate_education', type_='foreignkey')
    op.drop_table('majors')
    op.drop_column('candidate_education', 'major_id')
    op.drop_column('job_posts', 'majors')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('job_posts', sa.Column('majors', mysql.VARCHAR(length=100), nullable=True))
    op.add_column('candidate_education', sa.Column('major_id', mysql.INTEGER(), autoincrement=False, nullable=False))
    op.create_foreign_key('candidate_education_ibfk_1', 'candidate_education', 'majors', ['major_id'], ['id'])
    op.drop_column('candidate_education', 'major')
    op.drop_column('candidate_education', 'degree_level')
    op.create_table('majors',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', mysql.VARCHAR(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###