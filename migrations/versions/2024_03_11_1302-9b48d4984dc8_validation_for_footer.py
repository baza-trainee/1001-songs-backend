"""validation for footer

Revision ID: 9b48d4984dc8
Revises: 35588af2e18e
Create Date: 2024-03-11 13:02:34.322639

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from fastapi_storages.integrations.sqlalchemy import FileType


# revision identifiers, used by Alembic.
revision: str = "9b48d4984dc8"
down_revision: Union[str, None] = "35588af2e18e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "footer", "reporting", existing_type=sa.VARCHAR(length=500), nullable=False
    )
    op.alter_column(
        "footer", "privacy_policy", existing_type=sa.VARCHAR(), nullable=False
    )
    op.alter_column(
        "footer", "rules_and_terms", existing_type=sa.VARCHAR(), nullable=False
    )
    op.alter_column(
        "footer",
        "email",
        existing_type=sa.VARCHAR(length=100),
        type_=sa.String(length=35),
        nullable=False,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "footer",
        "email",
        existing_type=sa.String(length=35),
        type_=sa.VARCHAR(length=100),
        nullable=True,
    )
    op.alter_column(
        "footer", "rules_and_terms", existing_type=sa.VARCHAR(), nullable=True
    )
    op.alter_column(
        "footer", "privacy_policy", existing_type=sa.VARCHAR(), nullable=True
    )
    op.alter_column(
        "footer", "reporting", existing_type=sa.VARCHAR(length=500), nullable=True
    )
    # ### end Alembic commands ###