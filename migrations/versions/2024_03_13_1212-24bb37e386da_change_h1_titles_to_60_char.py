"""change h1 titles to 60 char

Revision ID: 24bb37e386da
Revises: c2444445cb93
Create Date: 2024-03-13 12:12:50.761654

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from fastapi_storages.integrations.sqlalchemy import FileType


# revision identifiers, used by Alembic.
revision: str = "24bb37e386da"
down_revision: Union[str, None] = "c2444445cb93"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "education_page",
        "title",
        existing_type=sa.VARCHAR(length=70),
        type_=sa.String(length=60),
        existing_nullable=False,
    )
    op.alter_column(
        "education_page_song_genres",
        "title",
        existing_type=sa.VARCHAR(length=70),
        type_=sa.String(length=60),
        existing_nullable=False,
    )
    op.alter_column(
        "expedition",
        "title",
        existing_type=sa.VARCHAR(length=70),
        type_=sa.String(length=60),
        existing_nullable=False,
    )
    op.alter_column(
        "expedition_info",
        "title",
        existing_type=sa.VARCHAR(length=70),
        type_=sa.String(length=60),
        existing_nullable=False,
    )
    op.alter_column(
        "news",
        "title",
        existing_type=sa.VARCHAR(length=70),
        type_=sa.String(length=60),
        existing_nullable=False,
    )
    op.alter_column(
        "our_projects",
        "title",
        existing_type=sa.VARCHAR(length=70),
        type_=sa.String(length=60),
        existing_nullable=False,
    )
    op.alter_column(
        "song",
        "title",
        existing_type=sa.VARCHAR(length=70),
        type_=sa.String(length=60),
        existing_nullable=False,
    )
    op.alter_column(
        "song_subcategories",
        "title",
        existing_type=sa.VARCHAR(length=70),
        type_=sa.String(length=60),
        existing_nullable=False,
    )
    op.alter_column(
        "song_subcategories", "media", existing_type=sa.VARCHAR(), nullable=False
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "song_subcategories", "media", existing_type=sa.VARCHAR(), nullable=True
    )
    op.alter_column(
        "song_subcategories",
        "title",
        existing_type=sa.String(length=60),
        type_=sa.VARCHAR(length=70),
        existing_nullable=False,
    )
    op.alter_column(
        "song",
        "title",
        existing_type=sa.String(length=60),
        type_=sa.VARCHAR(length=70),
        existing_nullable=False,
    )
    op.alter_column(
        "our_projects",
        "title",
        existing_type=sa.String(length=60),
        type_=sa.VARCHAR(length=70),
        existing_nullable=False,
    )
    op.alter_column(
        "news",
        "title",
        existing_type=sa.String(length=60),
        type_=sa.VARCHAR(length=70),
        existing_nullable=False,
    )
    op.alter_column(
        "expedition_info",
        "title",
        existing_type=sa.String(length=60),
        type_=sa.VARCHAR(length=70),
        existing_nullable=False,
    )
    op.alter_column(
        "expedition",
        "title",
        existing_type=sa.String(length=60),
        type_=sa.VARCHAR(length=70),
        existing_nullable=False,
    )
    op.alter_column(
        "education_page_song_genres",
        "title",
        existing_type=sa.String(length=60),
        type_=sa.VARCHAR(length=70),
        existing_nullable=False,
    )
    op.alter_column(
        "education_page",
        "title",
        existing_type=sa.String(length=60),
        type_=sa.VARCHAR(length=70),
        existing_nullable=False,
    )
    # ### end Alembic commands ###
