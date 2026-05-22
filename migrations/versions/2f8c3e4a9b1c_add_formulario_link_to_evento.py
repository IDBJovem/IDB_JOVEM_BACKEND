"""add formulario_link to evento

Revision ID: 2f8c3e4a9b1c
Revises: 2099c20fc4fc
Create Date: 2026-05-22 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2f8c3e4a9b1c"
down_revision: Union[str, Sequence[str], None] = "2099c20fc4fc"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("evento", sa.Column("formulario_link", sa.Text(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("evento", "formulario_link")
