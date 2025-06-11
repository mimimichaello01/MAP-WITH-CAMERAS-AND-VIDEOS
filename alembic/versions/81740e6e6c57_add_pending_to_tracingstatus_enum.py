"""Add Pending to TracingStatus enum

Revision ID: 81740e6e6c57
Revises: 99e1ade17d5c
Create Date: 2025-06-08 15:45:24.903017

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '81740e6e6c57'
down_revision: Union[str, None] = '99e1ade17d5c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("ALTER TYPE tracingstatus ADD VALUE IF NOT EXISTS 'PENDING';")


def downgrade() -> None:
    """Downgrade schema."""
    pass
