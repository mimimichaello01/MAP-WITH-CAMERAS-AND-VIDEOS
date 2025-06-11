"""Add Pending to TracingStatus enum

Revision ID: a2126fc6b963
Revises: 81740e6e6c57
Create Date: 2025-06-08 15:47:00.015350

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a2126fc6b963'
down_revision: Union[str, None] = '81740e6e6c57'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Добавить PENDING, если его ещё нет
    op.execute("ALTER TYPE tracingstatus ADD VALUE IF NOT EXISTS 'PENDING';")

    # 2. Создать новый enum без 'Pending'
    op.execute("CREATE TYPE tracingstatus_new AS ENUM ('PENDING', 'DONE', 'RUN', 'ERROR');")

    # 3. Обновить столбец на новый тип enum
    op.execute(
        "ALTER TABLE videos ALTER COLUMN tracing TYPE tracingstatus_new USING tracing::text::tracingstatus_new"
    )

    # 4. Удалить старый enum
    op.execute("DROP TYPE tracingstatus;")

    # 5. Переименовать новый enum обратно
    op.execute("ALTER TYPE tracingstatus_new RENAME TO tracingstatus;")


def downgrade() -> None:
    """Downgrade schema."""
    pass
