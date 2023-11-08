"""change to_do_list in project on task

Revision ID: 973e718d1e36
Revises: 26feeaaebd16
Create Date: 2023-10-30 11:20:11.557304

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '973e718d1e36'
down_revision = '26feeaaebd16'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('task',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.String(length=200), nullable=True),
    sa.Column('status', sa.Boolean(), nullable=True),
    sa.Column('urgency', sa.String(length=100), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('last_notification', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('to_do_list')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('to_do_list',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('description', sa.VARCHAR(length=200), autoincrement=False, nullable=True),
    sa.Column('status', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('urgency', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('last_notification', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], name='to_do_list_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='to_do_list_pkey')
    )
    op.drop_table('task')
    # ### end Alembic commands ###