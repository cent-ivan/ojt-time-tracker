"""empty message

Revision ID: c4501aca670e
Revises: 
Create Date: 2025-05-31 23:33:34.248085

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c4501aca670e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('adviserstbl',
    sa.Column('adviser_id', sa.String(length=255), nullable=False),
    sa.Column('adviser_name', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=50), nullable=False),
    sa.Column('school_name', sa.String(length=50), nullable=False),
    sa.Column('type', sa.String(length=50), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('adviser_id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('school_name')
    )
    op.create_table('schoolstbl',
    sa.Column('school_id', sa.Integer(), nullable=False),
    sa.Column('school_name', sa.String(length=50), nullable=False),
    sa.Column('adviser_id', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['adviser_id'], ['adviserstbl.adviser_id'], ),
    sa.PrimaryKeyConstraint('school_id'),
    sa.UniqueConstraint('school_name')
    )
    op.create_table('studentstbl',
    sa.Column('student_id', sa.String(length=255), nullable=False),
    sa.Column('student_name', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=50), nullable=False),
    sa.Column('school_id', sa.Integer(), nullable=True),
    sa.Column('company_name', sa.String(length=50), nullable=False),
    sa.Column('total_hours', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(length=50), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['school_id'], ['schoolstbl.school_id'], ),
    sa.PrimaryKeyConstraint('student_id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('student_name')
    )
    op.create_table('ojtlisttbl',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('student_id', sa.String(length=255), nullable=True),
    sa.Column('school_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['school_id'], ['schoolstbl.school_id'], ),
    sa.ForeignKeyConstraint(['student_id'], ['studentstbl.student_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('timesheettbl',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('student_id', sa.String(length=255), nullable=True),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('time_in', sa.Time(), nullable=True),
    sa.Column('time_out', sa.Time(), nullable=True),
    sa.Column('hours_worked', sa.Integer(), nullable=True),
    sa.Column('status', sa.String(length=30), nullable=True),
    sa.Column('note', sa.String(length=50), nullable=True),
    sa.ForeignKeyConstraint(['student_id'], ['studentstbl.student_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('timesheettbl', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_timesheettbl_date'), ['date'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('timesheettbl', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_timesheettbl_date'))

    op.drop_table('timesheettbl')
    op.drop_table('ojtlisttbl')
    op.drop_table('studentstbl')
    op.drop_table('schoolstbl')
    op.drop_table('adviserstbl')
    # ### end Alembic commands ###
