"""merge heads dev

Revision ID: d57223d3687b
Revises: 53b81befb540, 56cf2bb92295
Create Date: 2026-05-26 22:44:00.030526

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd57223d3687b'
down_revision: Union[str, Sequence[str], None] = ('53b81befb540', '56cf2bb92295')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
