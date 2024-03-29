"""add footer and our_team

Revision ID: 16d28d1a4470
Revises: 087aca92b2d3
Create Date: 2024-02-09 18:51:39.463511

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from fastapi_storages.integrations.sqlalchemy import FileType
from fastapi_storages import FileSystemStorage

# revision identifiers, used by Alembic.
revision: str = "16d28d1a4470"
down_revision: Union[str, None] = "087aca92b2d3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


storage1 = FileSystemStorage(path="static/media/footer")
storage2 = FileSystemStorage(path="static/media/our_team")


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "footer",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("reporting", sa.String(length=500), nullable=True),
        sa.Column("qr_code_url", FileType(storage1), nullable=True),
        sa.Column("privacy_policy", FileType(storage1), nullable=True),
        sa.Column("rules_and_terms", FileType(storage1), nullable=True),
        sa.Column("email", sa.String(length=100), nullable=True),
        sa.Column("facebook_url", sa.String(length=500), nullable=True),
        sa.Column("youtube_url", sa.String(length=500), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "our_team",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("full_name", sa.String(length=100), nullable=False),
        sa.Column("photo", FileType(storage2), nullable=True),
        sa.Column("description", sa.String(length=500), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("our_team")
    op.drop_table("footer")
    # ### end Alembic commands ###
