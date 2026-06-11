"""create lider table

Revision ID: b7d4e1f9a3c2
Revises: f1a2b3c4d5e6
Create Date: 2026-06-11 14:10:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b7d4e1f9a3c2"
down_revision: Union[str, Sequence[str], None] = "f1a2b3c4d5e6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "lider",
        sa.Column("lider_id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("nome", sa.Text(), nullable=False),
        sa.Column("cargo", sa.Text(), nullable=False),
        sa.Column("imagem_url", sa.Text(), nullable=True),
        sa.Column("is_antigo", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("ordem", sa.Integer(), nullable=False, server_default="0"),
        sa.PrimaryKeyConstraint("lider_id"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("lider")
