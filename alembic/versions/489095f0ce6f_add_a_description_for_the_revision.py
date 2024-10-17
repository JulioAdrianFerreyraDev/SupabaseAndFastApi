"""Add a description for the revision

Revision ID: 489095f0ce6f
Revises: 
Create Date: 2024-10-10 00:50:55.270810

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '489095f0ce6f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("roles", sa.Column(sa.Integer, name="role_id", primary_key=True),
                    sa.Column(sa.String, name="role", nullable=False), if_not_exists=True)


def downgrade() -> None:
    op.drop_table(table_name="roles", if_exists=True)
