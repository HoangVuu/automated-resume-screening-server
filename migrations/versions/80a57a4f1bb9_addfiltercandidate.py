"""addFilterCandidate

Revision ID: 80a57a4f1bb9
Revises: 32836839317c
Create Date: 2020-12-28 23:21:26.683339

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '80a57a4f1bb9'
down_revision = '32836839317c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('filter_candidates',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('job_domains', sa.String(length=100), nullable=True),
    sa.Column('provinces', sa.String(length=100), nullable=True),
    sa.Column('atleast_skills', sa.String(length=300), nullable=True),
    sa.Column('required_skills', sa.String(length=300), nullable=True),
    sa.Column('not_allowed_skills', sa.String(length=300), nullable=True),
    sa.Column('min_year', sa.String(length=10), nullable=True),
    sa.Column('max_year', sa.String(length=10), nullable=True),
    sa.Column('gender', sa.Boolean(), nullable=True),
    sa.Column('months_of_experience', sa.Integer(), nullable=True),
    sa.Column('last_edit', sa.DateTime(), nullable=False),
    sa.Column('recruiter_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['recruiter_id'], ['recruiters.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('filter_candidates')
    # ### end Alembic commands ###
