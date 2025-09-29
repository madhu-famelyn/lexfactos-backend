"""added extra field in lawyer registration 1 at 3:19 9/5/2025

Revision ID: 773ca6363312
Revises: dd29bd595094
Create Date: 2025-09-25 15:19:50.362754

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '773ca6363312'
down_revision: Union[str, Sequence[str], None] = 'dd29bd595094'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    """Upgrade schema."""
    pass  # Column already exists manually



def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('lawyerRegistration1', 'short_note')
