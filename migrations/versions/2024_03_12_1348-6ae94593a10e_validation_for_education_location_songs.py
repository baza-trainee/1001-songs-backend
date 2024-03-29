"""validation for education, location, songs

Revision ID: 6ae94593a10e
Revises: ac84c4af01aa
Create Date: 2024-03-12 13:48:56.677359

"""

from typing import Sequence, Union

from alembic import op
from fastapi_storages import FileSystemStorage
import sqlalchemy as sa
from fastapi_storages.integrations.sqlalchemy import FileType
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "6ae94593a10e"
down_revision: Union[str, None] = "ac84c4af01aa"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

song_storage = FileSystemStorage(path="static/media/song")
education_storage = FileSystemStorage(path="static/media/education_page_song_genres")


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "calendar_and_ritual_categories",
        "title",
        existing_type=sa.VARCHAR(length=100),
        type_=sa.String(length=50),
        nullable=False,
    )
    op.alter_column(
        "calendar_and_ritual_categories",
        "media",
        existing_type=sa.VARCHAR(),
        nullable=False,
    )
    op.alter_column(
        "calendar_and_ritual_categories",
        "description",
        existing_type=sa.VARCHAR(length=2000),
        nullable=False,
    )
    op.alter_column(
        "cities",
        "name",
        existing_type=sa.VARCHAR(length=100),
        type_=sa.String(length=50),
        existing_nullable=False,
    )
    op.alter_column(
        "cities",
        "latitude",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        nullable=False,
    )
    op.alter_column(
        "cities",
        "longitude",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        nullable=False,
    )
    op.alter_column(
        "countries",
        "name",
        existing_type=sa.VARCHAR(length=100),
        type_=sa.String(length=50),
        existing_nullable=False,
    )
    op.alter_column(
        "education_page",
        "title",
        existing_type=sa.VARCHAR(length=100),
        type_=sa.String(length=70),
        nullable=False,
    )
    op.alter_column(
        "education_page",
        "description",
        existing_type=sa.VARCHAR(length=5000),
        type_=sa.String(length=600),
        nullable=False,
    )
    op.alter_column(
        "education_page",
        "recommendations",
        existing_type=sa.VARCHAR(length=10000),
        nullable=False,
    )
    op.add_column(
        "education_page_song_genres",
        sa.Column("media4", FileType(education_storage), nullable=True),
    )
    op.add_column(
        "education_page_song_genres",
        sa.Column("media5", FileType(education_storage), nullable=True),
    )
    op.alter_column(
        "education_page_song_genres",
        "title",
        existing_type=sa.VARCHAR(length=100),
        type_=sa.String(length=70),
        existing_nullable=False,
    )
    op.alter_column(
        "education_page_song_genres",
        "description",
        existing_type=sa.VARCHAR(length=2000),
        nullable=False,
    )
    op.alter_column(
        "education_page_song_genres",
        "media1",
        existing_type=sa.VARCHAR(),
        nullable=False,
    )
    op.alter_column(
        "education_page_song_genres",
        "media2",
        existing_type=sa.VARCHAR(),
        nullable=False,
    )
    op.alter_column(
        "education_page_song_genres",
        "media3",
        existing_type=sa.VARCHAR(),
        nullable=False,
    )
    op.alter_column(
        "funds",
        "title",
        existing_type=sa.VARCHAR(length=100),
        type_=sa.String(length=50),
        existing_nullable=False,
    )
    op.alter_column(
        "genre",
        "genre_name",
        existing_type=sa.VARCHAR(length=100),
        type_=sa.String(length=50),
        nullable=False,
    )
    op.alter_column(
        "regions",
        "name",
        existing_type=sa.VARCHAR(length=100),
        type_=sa.String(length=50),
        existing_nullable=False,
    )
    op.add_column("song", sa.Column("photo4", FileType(song_storage), nullable=True))
    op.add_column("song", sa.Column("photo5", FileType(song_storage), nullable=True))
    op.add_column(
        "song", sa.Column("ethnographic_photo4", FileType(song_storage), nullable=True)
    )
    op.add_column(
        "song", sa.Column("ethnographic_photo5", FileType(song_storage), nullable=True)
    )
    op.alter_column(
        "song",
        "title",
        existing_type=sa.VARCHAR(length=200),
        type_=sa.String(length=70),
        nullable=False,
    )
    op.alter_column(
        "song",
        "song_description",
        existing_type=sa.VARCHAR(length=2000),
        type_=sa.String(length=200),
        existing_nullable=True,
    )
    op.alter_column("song", "recording_date", existing_type=sa.DATE(), nullable=False)
    op.alter_column(
        "song", "performers", existing_type=sa.VARCHAR(length=200), nullable=False
    )
    op.alter_column(
        "song",
        "ethnographic_district",
        existing_type=sa.VARCHAR(length=100),
        type_=sa.String(length=50),
        nullable=False,
    )
    op.alter_column(
        "song",
        "collectors",
        existing_type=postgresql.ARRAY(sa.VARCHAR(length=100)),
        type_=sa.ARRAY(sa.String(length=25)),
        nullable=False,
    )
    op.alter_column(
        "song",
        "video_url",
        existing_type=sa.VARCHAR(length=1000),
        type_=sa.String(length=500),
        existing_nullable=True,
    )
    op.alter_column(
        "song",
        "comment_map",
        existing_type=sa.VARCHAR(length=500),
        type_=sa.String(length=200),
        existing_nullable=True,
    )
    op.alter_column("song", "photo1", existing_type=sa.VARCHAR(), nullable=False)
    op.alter_column(
        "song", "ethnographic_photo1", existing_type=sa.VARCHAR(), nullable=False
    )
    op.drop_column("song", "recording_location")
    op.alter_column(
        "song_subcategories",
        "title",
        existing_type=sa.VARCHAR(length=100),
        type_=sa.String(length=70),
        existing_nullable=False,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "song_subcategories",
        "title",
        existing_type=sa.String(length=70),
        type_=sa.VARCHAR(length=100),
        existing_nullable=False,
    )
    op.add_column(
        "song",
        sa.Column(
            "recording_location",
            sa.VARCHAR(length=100),
            autoincrement=False,
            nullable=True,
        ),
    )
    op.alter_column(
        "song", "ethnographic_photo1", existing_type=sa.VARCHAR(), nullable=True
    )
    op.alter_column("song", "photo1", existing_type=sa.VARCHAR(), nullable=True)
    op.alter_column(
        "song",
        "comment_map",
        existing_type=sa.String(length=200),
        type_=sa.VARCHAR(length=500),
        existing_nullable=True,
    )
    op.alter_column(
        "song",
        "video_url",
        existing_type=sa.String(length=500),
        type_=sa.VARCHAR(length=1000),
        existing_nullable=True,
    )
    op.alter_column(
        "song",
        "collectors",
        existing_type=sa.ARRAY(sa.String(length=25)),
        type_=postgresql.ARRAY(sa.VARCHAR(length=100)),
        nullable=True,
    )
    op.alter_column(
        "song",
        "ethnographic_district",
        existing_type=sa.String(length=50),
        type_=sa.VARCHAR(length=100),
        nullable=True,
    )
    op.alter_column(
        "song", "performers", existing_type=sa.VARCHAR(length=200), nullable=True
    )
    op.alter_column("song", "recording_date", existing_type=sa.DATE(), nullable=True)
    op.alter_column(
        "song",
        "song_description",
        existing_type=sa.String(length=200),
        type_=sa.VARCHAR(length=2000),
        existing_nullable=True,
    )
    op.alter_column(
        "song",
        "title",
        existing_type=sa.String(length=70),
        type_=sa.VARCHAR(length=200),
        nullable=True,
    )
    op.drop_column("song", "ethnographic_photo5")
    op.drop_column("song", "ethnographic_photo4")
    op.drop_column("song", "photo5")
    op.drop_column("song", "photo4")
    op.alter_column(
        "regions",
        "name",
        existing_type=sa.String(length=50),
        type_=sa.VARCHAR(length=100),
        existing_nullable=False,
    )
    op.alter_column(
        "genre",
        "genre_name",
        existing_type=sa.String(length=50),
        type_=sa.VARCHAR(length=100),
        nullable=True,
    )
    op.alter_column(
        "funds",
        "title",
        existing_type=sa.String(length=50),
        type_=sa.VARCHAR(length=100),
        existing_nullable=False,
    )
    op.alter_column(
        "education_page_song_genres",
        "media3",
        existing_type=sa.VARCHAR(),
        nullable=True,
    )
    op.alter_column(
        "education_page_song_genres",
        "media2",
        existing_type=sa.VARCHAR(),
        nullable=True,
    )
    op.alter_column(
        "education_page_song_genres",
        "media1",
        existing_type=sa.VARCHAR(),
        nullable=True,
    )
    op.alter_column(
        "education_page_song_genres",
        "description",
        existing_type=sa.VARCHAR(length=2000),
        nullable=True,
    )
    op.alter_column(
        "education_page_song_genres",
        "title",
        existing_type=sa.String(length=70),
        type_=sa.VARCHAR(length=100),
        existing_nullable=False,
    )
    op.drop_column("education_page_song_genres", "media5")
    op.drop_column("education_page_song_genres", "media4")
    op.alter_column(
        "education_page",
        "recommendations",
        existing_type=sa.VARCHAR(length=10000),
        nullable=True,
    )
    op.alter_column(
        "education_page",
        "description",
        existing_type=sa.String(length=600),
        type_=sa.VARCHAR(length=5000),
        nullable=True,
    )
    op.alter_column(
        "education_page",
        "title",
        existing_type=sa.String(length=70),
        type_=sa.VARCHAR(length=100),
        nullable=True,
    )
    op.alter_column(
        "countries",
        "name",
        existing_type=sa.String(length=50),
        type_=sa.VARCHAR(length=100),
        existing_nullable=False,
    )
    op.alter_column(
        "cities",
        "longitude",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        nullable=True,
    )
    op.alter_column(
        "cities",
        "latitude",
        existing_type=sa.DOUBLE_PRECISION(precision=53),
        nullable=True,
    )
    op.alter_column(
        "cities",
        "name",
        existing_type=sa.String(length=50),
        type_=sa.VARCHAR(length=100),
        existing_nullable=False,
    )
    op.alter_column(
        "calendar_and_ritual_categories",
        "description",
        existing_type=sa.VARCHAR(length=2000),
        nullable=True,
    )
    op.alter_column(
        "calendar_and_ritual_categories",
        "media",
        existing_type=sa.VARCHAR(),
        nullable=True,
    )
    op.alter_column(
        "calendar_and_ritual_categories",
        "title",
        existing_type=sa.String(length=50),
        type_=sa.VARCHAR(length=100),
        nullable=True,
    )
    # ### end Alembic commands ###
