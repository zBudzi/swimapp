"""empty message

Revision ID: a5c0e15ccdbd
Revises: 
Create Date: 2022-09-19 18:38:52.546656

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a5c0e15ccdbd'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('swims',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('kraulen_bahnen', sa.Integer(), nullable=False),
    sa.Column('kraulen_bahnen_zeit', sa.Float(), nullable=True),
    sa.Column('brust_bahnen', sa.Integer(), nullable=False),
    sa.Column('brust_bahnen_zeit', sa.Float(), nullable=True),
    sa.Column('ruecken_bahnen', sa.Integer(), nullable=False),
    sa.Column('ruecken_bahnen_zeit', sa.Float(), nullable=True),
    sa.Column('kommentar', sa.String(), nullable=True),
    sa.Column('bahnlaenge', sa.Integer(), nullable=False),
    sa.Column('kcal', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('swims')
    # ### end Alembic commands ###
