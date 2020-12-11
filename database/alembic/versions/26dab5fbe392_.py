"""empty message

Revision ID: 26dab5fbe392
Revises: 
Create Date: 2020-12-08 20:48:52.724119

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '26dab5fbe392'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('event_user',
    sa.Column('id_event_user', sa.Integer(), nullable=False),
    sa.Column('events', sa.ARRAY(sa.Integer()), nullable=True),
    sa.Column('users', sa.ARRAY(sa.Integer()), nullable=True),
    sa.Column('access', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id_event_user')
    )
    op.create_table('events',
    sa.Column('id_event', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('status', sa.ARRAY(sa.String()), nullable=True),
    sa.PrimaryKeyConstraint('id_event')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('firstname', sa.String(), nullable=True),
    sa.Column('lastname', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.Column('phone', sa.String(), nullable=True),
    sa.Column('userstatus', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    op.drop_table('events')
    op.drop_table('event_user')
    # ### end Alembic commands ###
