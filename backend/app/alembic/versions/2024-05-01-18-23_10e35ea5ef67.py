"""added swipe settings models

Revision ID: 10e35ea5ef67
Revises: 6b1832d1d005
Create Date: 2024-05-01 18:23:44.294908

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils
import sqlmodel # added


# revision identifiers, used by Alembic.
revision = '10e35ea5ef67'
down_revision = '6b1832d1d005'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm") 
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('SwipeSettings',
    sa.Column('id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('gender_preferences', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('age_range_start', sa.BigInteger(), server_default='0', nullable=True),
    sa.Column('age_range_end', sa.BigInteger(), server_default='0', nullable=True),
    sa.Column('swipe_right_ratio', sa.BigInteger(), server_default='0', nullable=True),
    sa.Column('swipe_delay', sa.BigInteger(), server_default='0', nullable=True),
    sa.Column('project_id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.ForeignKeyConstraint(['project_id'], ['Project.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_SwipeSettings_id'), 'SwipeSettings', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_SwipeSettings_id'), table_name='SwipeSettings')
    op.drop_table('SwipeSettings')
    # ### end Alembic commands ###
