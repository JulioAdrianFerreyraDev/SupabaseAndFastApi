"""Add a description for the revision

Revision ID: 489095f0ce6f
Revises: 
Create Date: 2024-10-10 00:50:55.270810

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '489095f0ce6f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(table_name="sales", column_name="total_price", new_column_name="total")

def downgrade() -> None:
    op.alter_column(table_name="sales", column_name="total", new_column_name="total_price")
