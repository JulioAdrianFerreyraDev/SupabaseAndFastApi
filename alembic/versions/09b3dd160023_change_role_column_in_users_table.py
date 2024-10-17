"""change role column in users table

Revision ID: 09b3dd160023
Revises: f00ca63a3fd0
Create Date: 2024-10-17 12:36:20.333958

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '09b3dd160023'
down_revision: Union[str, None] = 'f00ca63a3fd0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(column_name="role", table_name="users", new_column_name="role_id")


def downgrade() -> None:
    op.alter_column(column_name="role_id", table_name="users", new_column_name="role")
