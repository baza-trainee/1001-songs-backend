"""add ethnographic_photos

Revision ID: 99cf242221d4
Revises: 67625f5934df
Create Date: 2024-02-16 00:40:40.022079

"""

from typing import Sequence, Union

from alembic import op
from fastapi_storages import FileSystemStorage
import sqlalchemy as sa
from fastapi_storages.integrations.sqlalchemy import FileType


# revision identifiers, used by Alembic.
revision: str = "99cf242221d4"
down_revision: Union[str, None] = "67625f5934df"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None
storage = FileSystemStorage(path="static/media/song")


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "song", sa.Column("ethnographic_photo1", FileType(storage), nullable=True)
    )
    op.add_column(
        "song", sa.Column("ethnographic_photo2", FileType(storage), nullable=True)
    )
    op.add_column(
        "song", sa.Column("ethnographic_photo3", FileType(storage), nullable=True)
    )
    op.drop_column("song", "source")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "song",
        sa.Column("source", sa.VARCHAR(length=200), autoincrement=False, nullable=True),
    )
    op.drop_column("song", "ethnographic_photo3")
    op.drop_column("song", "ethnographic_photo2")
    op.drop_column("song", "ethnographic_photo1")
    # ### end Alembic commands ###
