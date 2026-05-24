"""merge heads

Revision ID: c78f37024085
Revises: 2005387ea9c7, beb08b5adb27
Create Date: 2026-05-24 02:41:10.776898

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c78f37024085'
down_revision: Union[str, Sequence[str], None] = ('2005387ea9c7', 'beb08b5adb27')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
