"""change status_code to integer

Revision ID: a78ec7045aba
Revises: c60221957020
Create Date: 2026-03-15 16:08:23.526860

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a78ec7045aba'
down_revision: Union[str, Sequence[str], None] = 'c60221957020'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column('request_logs', 'status_code',
               existing_type=sa.VARCHAR(),
               type_=sa.Integer(),
               postgresql_using='status_code::integer', # This is the magic line
               existing_nullable=True)


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column('request_logs', 'status_code',
               existing_type=sa.Integer(),
               type_=sa.VARCHAR(),
               postgresql_using='status_code::text',
               existing_nullable=True)
