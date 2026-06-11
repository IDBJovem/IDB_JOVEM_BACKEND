"""add link_imagem to evento and produto

Revision ID: f1a2b3c4d5e6
Revises: d57223d3687b
Create Date: 2026-06-10 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f1a2b3c4d5e6"
down_revision: Union[str, Sequence[str], None] = "d57223d3687b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("evento", sa.Column("link_imagem", sa.Text(), nullable=True))
    op.add_column("produto", sa.Column("link_imagem", sa.Text(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("produto", "link_imagem")
    op.drop_column("evento", "link_imagem")
