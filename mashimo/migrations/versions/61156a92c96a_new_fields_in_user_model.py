"""new fields in user model

Revision ID: 61156a92c96a
Revises: 1fa84f029e64
Create Date: 2024-05-07 14:57:09.418389

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '61156a92c96a'
down_revision = '1fa84f029e64'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('about_me', sa.String(length=140), nullable=True))
        batch_op.add_column(sa.Column('last_seen', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('last_seen')
        batch_op.drop_column('about_me')

    # ### end Alembic commands ###
