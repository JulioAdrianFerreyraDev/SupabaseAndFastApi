"""add categories-products relationship table

Revision ID: 59bf5d3457d0
Revises: 32ccb8aa3523
Create Date: 2024-10-18 19:48:03.545446

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '59bf5d3457d0'
down_revision: Union[str, None] = '32ccb8aa3523'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("categories-products", sa.Column(sa.Integer, primary_key=True, name="cp_id"),
                    sa.Column(sa.Integer, sa.ForeignKey("products.product_id"), name="product_id"),
                    sa.Column(sa.Integer, sa.ForeignKey("categories.category_id"), name="category_id"),
                    if_not_exists=True)


def downgrade() -> None:
    op.drop_table(table_name="categories-products", if_exists=True)
