"""validation for project, our_team, news, expedition

Revision ID: ac84c4af01aa
Revises: 5304409cf611
Create Date: 2024-03-12 11:02:25.810190

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from fastapi_storages.integrations.sqlalchemy import FileType
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "ac84c4af01aa"
down_revision: Union[str, None] = "5304409cf611"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "expedition",
        "title",
        existing_type=sa.VARCHAR(length=250),
        type_=sa.String(length=70),
        existing_nullable=False,
    )
    op.alter_column(
        "expedition",
        "short_description",
        existing_type=sa.VARCHAR(length=120),
        type_=sa.String(length=200),
        existing_nullable=False,
    )
    op.alter_column(
        "expedition", "map_photo", existing_type=sa.VARCHAR(), nullable=False
    )
    op.alter_column(
        "expedition", "preview_photo", existing_type=sa.VARCHAR(), nullable=False
    )
    op.alter_column(
        "expedition", "expedition_date", existing_type=sa.DATE(), nullable=False
    )
    op.alter_column(
        "expedition",
        "authors",
        existing_type=postgresql.ARRAY(sa.VARCHAR(length=100)),
        nullable=False,
    )
    op.alter_column(
        "news",
        "title",
        existing_type=sa.VARCHAR(length=250),
        type_=sa.String(length=70),
        existing_nullable=False,
    )
    op.alter_column(
        "news",
        "short_description",
        existing_type=sa.VARCHAR(length=120),
        type_=sa.String(length=200),
        existing_nullable=False,
    )
    op.alter_column(
        "news",
        "authors",
        existing_type=postgresql.ARRAY(sa.VARCHAR(length=100)),
        type_=sa.ARRAY(sa.String(length=25)),
        nullable=False,
    )
    op.alter_column(
        "news",
        "editors",
        existing_type=postgresql.ARRAY(sa.VARCHAR(length=100)),
        type_=sa.ARRAY(sa.String(length=25)),
        existing_nullable=True,
    )
    op.alter_column(
        "news",
        "photographers",
        existing_type=postgresql.ARRAY(sa.VARCHAR(length=100)),
        type_=sa.ARRAY(sa.String(length=25)),
        existing_nullable=True,
    )
    op.alter_column("news", "preview_photo", existing_type=sa.VARCHAR(), nullable=False)
    op.alter_column(
        "our_projects",
        "title",
        existing_type=sa.VARCHAR(length=100),
        type_=sa.String(length=70),
        existing_nullable=False,
    )
    op.alter_column(
        "our_projects",
        "short_description",
        existing_type=sa.VARCHAR(length=120),
        type_=sa.String(length=200),
        existing_nullable=False,
    )
    op.alter_column(
        "our_projects", "preview_photo", existing_type=sa.VARCHAR(), nullable=False
    )
    op.alter_column(
        "our_projects", "project_date", existing_type=sa.DATE(), nullable=False
    )
    op.alter_column(
        "our_projects",
        "authors",
        existing_type=postgresql.ARRAY(sa.VARCHAR(length=100)),
        type_=sa.ARRAY(sa.String(length=25)),
        nullable=False,
    )
    op.alter_column(
        "our_projects",
        "editors",
        existing_type=postgresql.ARRAY(sa.VARCHAR(length=100)),
        type_=sa.ARRAY(sa.String(length=25)),
        existing_nullable=True,
    )
    op.alter_column(
        "our_projects",
        "photographers",
        existing_type=postgresql.ARRAY(sa.VARCHAR(length=100)),
        type_=sa.ARRAY(sa.String(length=25)),
        existing_nullable=True,
    )
    op.drop_column("our_projects", "recording")
    op.alter_column(
        "our_team",
        "full_name",
        existing_type=sa.VARCHAR(length=100),
        type_=sa.String(length=50),
        existing_nullable=False,
    )
    op.alter_column("our_team", "photo", existing_type=sa.VARCHAR(), nullable=False)
    op.alter_column(
        "our_team",
        "description",
        existing_type=sa.VARCHAR(length=500),
        type_=sa.String(length=300),
        nullable=False,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "our_team",
        "description",
        existing_type=sa.String(length=300),
        type_=sa.VARCHAR(length=500),
        nullable=True,
    )
    op.alter_column("our_team", "photo", existing_type=sa.VARCHAR(), nullable=True)
    op.alter_column(
        "our_team",
        "full_name",
        existing_type=sa.String(length=50),
        type_=sa.VARCHAR(length=100),
        existing_nullable=False,
    )
    op.add_column(
        "our_projects",
        sa.Column(
            "recording",
            postgresql.ARRAY(sa.VARCHAR(length=100)),
            autoincrement=False,
            nullable=True,
        ),
    )
    op.alter_column(
        "our_projects",
        "photographers",
        existing_type=sa.ARRAY(sa.String(length=25)),
        type_=postgresql.ARRAY(sa.VARCHAR(length=100)),
        existing_nullable=True,
    )
    op.alter_column(
        "our_projects",
        "editors",
        existing_type=sa.ARRAY(sa.String(length=25)),
        type_=postgresql.ARRAY(sa.VARCHAR(length=100)),
        existing_nullable=True,
    )
    op.alter_column(
        "our_projects",
        "authors",
        existing_type=sa.ARRAY(sa.String(length=25)),
        type_=postgresql.ARRAY(sa.VARCHAR(length=100)),
        nullable=True,
    )
    op.alter_column(
        "our_projects", "project_date", existing_type=sa.DATE(), nullable=True
    )
    op.alter_column(
        "our_projects", "preview_photo", existing_type=sa.VARCHAR(), nullable=True
    )
    op.alter_column(
        "our_projects",
        "short_description",
        existing_type=sa.String(length=200),
        type_=sa.VARCHAR(length=120),
        existing_nullable=False,
    )
    op.alter_column(
        "our_projects",
        "title",
        existing_type=sa.String(length=70),
        type_=sa.VARCHAR(length=100),
        existing_nullable=False,
    )
    op.alter_column("news", "preview_photo", existing_type=sa.VARCHAR(), nullable=True)
    op.alter_column(
        "news",
        "photographers",
        existing_type=sa.ARRAY(sa.String(length=25)),
        type_=postgresql.ARRAY(sa.VARCHAR(length=100)),
        existing_nullable=True,
    )
    op.alter_column(
        "news",
        "editors",
        existing_type=sa.ARRAY(sa.String(length=25)),
        type_=postgresql.ARRAY(sa.VARCHAR(length=100)),
        existing_nullable=True,
    )
    op.alter_column(
        "news",
        "authors",
        existing_type=sa.ARRAY(sa.String(length=25)),
        type_=postgresql.ARRAY(sa.VARCHAR(length=100)),
        nullable=True,
    )
    op.alter_column(
        "news",
        "short_description",
        existing_type=sa.String(length=200),
        type_=sa.VARCHAR(length=120),
        existing_nullable=False,
    )
    op.alter_column(
        "news",
        "title",
        existing_type=sa.String(length=70),
        type_=sa.VARCHAR(length=250),
        existing_nullable=False,
    )
    op.alter_column(
        "expedition",
        "authors",
        existing_type=postgresql.ARRAY(sa.VARCHAR(length=100)),
        nullable=True,
    )
    op.alter_column(
        "expedition", "expedition_date", existing_type=sa.DATE(), nullable=True
    )
    op.alter_column(
        "expedition", "preview_photo", existing_type=sa.VARCHAR(), nullable=True
    )
    op.alter_column(
        "expedition", "map_photo", existing_type=sa.VARCHAR(), nullable=True
    )
    op.alter_column(
        "expedition",
        "short_description",
        existing_type=sa.String(length=200),
        type_=sa.VARCHAR(length=120),
        existing_nullable=False,
    )
    op.alter_column(
        "expedition",
        "title",
        existing_type=sa.String(length=70),
        type_=sa.VARCHAR(length=250),
        existing_nullable=False,
    )
    # ### end Alembic commands ###
