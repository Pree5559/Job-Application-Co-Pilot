"""initial migration

Revision ID: 0001_initial
Revises: 
Create Date: 2026-06-07
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('username', sa.String(), nullable=False, unique=True),
        sa.Column('hashed_password', sa.String(), nullable=False),
    )

    op.create_table(
        'applications',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('job_title', sa.String(), nullable=False),
        sa.Column('company', sa.String(), nullable=False),
        sa.Column('jd_text', sa.Text(), nullable=False),
        sa.Column('jd_url', sa.String(), nullable=True),
        sa.Column('original_resume_text', sa.Text(), nullable=False),
        sa.Column('resume_sections', sa.Text(), nullable=True),
        sa.Column('status', sa.String(), nullable=True, server_default=sa.text("'not yet'")),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id')),
    )

    op.create_table(
        'drafts',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('application_id', sa.Integer(), sa.ForeignKey('applications.id'), unique=True),
        sa.Column('fit_analysis', sa.Text(), nullable=True),
        sa.Column('resume_rewrite', sa.Text(), nullable=True),
        sa.Column('cover_letter', sa.Text(), nullable=True),
        sa.Column('interview_qa', sa.Text(), nullable=True),
        sa.Column('ats_score', sa.Text(), nullable=True),
    )


def downgrade():
    op.drop_table('drafts')
    op.drop_table('applications')
    op.drop_table('users')
