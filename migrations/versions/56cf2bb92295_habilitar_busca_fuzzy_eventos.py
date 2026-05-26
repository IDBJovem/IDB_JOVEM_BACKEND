"""habilitar busca fuzzy eventos

Revision ID: 56cf2bb92295
Revises: 4c2346676f0f
Create Date: 2026-05-26 00:17:26.190607

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '56cf2bb92295'
down_revision: Union[str, Sequence[str], None] = '4c2346676f0f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm")


def downgrade():
    op.execute("DROP EXTENSION IF EXISTS pg_trgm")
