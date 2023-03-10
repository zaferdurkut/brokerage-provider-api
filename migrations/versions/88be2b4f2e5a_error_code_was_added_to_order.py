"""error_code was added to order

Revision ID: 88be2b4f2e5a
Revises: 40d75e76f454
Create Date: 2023-01-23 00:13:19.045663

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "88be2b4f2e5a"
down_revision = "40d75e76f454"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("order", sa.Column("error_code", sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("order", "error_code")
    # ### end Alembic commands ###
