"""rename userid/createdat columns in user_blacklist_inn

Revision ID: 6fdf6afd7f77
Revises: de99d41dff72
Create Date: 2025-12-14 14:57:50.089833

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '6fdf6afd7f77'
down_revision: Union[str, None] = 'de99d41dff72'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    pass

def downgrade() -> None:
    pass
