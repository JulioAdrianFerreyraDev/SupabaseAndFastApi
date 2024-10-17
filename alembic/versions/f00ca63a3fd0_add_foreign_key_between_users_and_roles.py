"""add foreign key between users and roles

Revision ID: f00ca63a3fd0
Revises: 489095f0ce6f
Create Date: 2024-10-17 12:25:56.146757

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'f00ca63a3fd0'
down_revision: Union[str, None] = '489095f0ce6f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(table_name="users",
                  column=sa.Column(sa.Integer, sa.ForeignKey("roles.role_id"), name="role", default=1, nullable=True))


def downgrade() -> None:
    op.drop_column(table_name="users", column_name="role")
