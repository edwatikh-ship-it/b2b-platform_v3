"""create request_recipients table

Revision ID: ea4ad222417f
Revises: bbff04c57403
Create Date: 2025-12-14 09:33:37.835684

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'ea4ad222417f'
down_revision: Union[str, None] = 'bbff04c57403'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    pass

def downgrade() -> None:
    pass
