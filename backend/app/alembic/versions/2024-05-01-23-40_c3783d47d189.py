"""added conversation model

Revision ID: c3783d47d189
Revises: b478fdf1a4fd
Create Date: 2024-05-01 23:40:49.599471

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils
import sqlmodel # added


# revision identifiers, used by Alembic.
revision = 'c3783d47d189'
down_revision = 'b478fdf1a4fd'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm") 
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Conversation',
    sa.Column('fan_name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('fan_url', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('status', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('account_id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.ForeignKeyConstraint(['account_id'], ['Account.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_Conversation_id'), 'Conversation', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_Conversation_id'), table_name='Conversation')
    op.drop_table('Conversation')
    # ### end Alembic commands ###
