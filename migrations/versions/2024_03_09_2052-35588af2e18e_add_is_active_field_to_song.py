"""add is_active field to song

Revision ID: 35588af2e18e
Revises: 8d3d8cd4f4b4
Create Date: 2024-03-09 20:52:30.881391

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from fastapi_storages.integrations.sqlalchemy import FileType


# revision identifiers, used by Alembic.
revision: str = "35588af2e18e"
down_revision: Union[str, None] = "8d3d8cd4f4b4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("song", sa.Column("is_active", sa.Boolean(), nullable=False))
    op.drop_column("song", "archive")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "song",
        sa.Column(
            "archive", sa.VARCHAR(length=255), autoincrement=False, nullable=True
        ),
    )
    op.drop_column("song", "is_active")
    # ### end Alembic commands ###
