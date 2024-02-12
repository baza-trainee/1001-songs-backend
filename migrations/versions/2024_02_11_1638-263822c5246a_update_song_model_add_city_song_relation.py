"""update song model, add city&song relation

Revision ID: 263822c5246a
Revises: 64820a3923c0
Create Date: 2024-02-11 16:38:10.152725

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "263822c5246a"
down_revision: Union[str, None] = "64820a3923c0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "genre",
        "genre_name",
        existing_type=sa.VARCHAR(length=50),
        type_=sa.String(length=100),
        existing_nullable=True,
    )
    op.add_column("song", sa.Column("song_text", sa.String(length=2000), nullable=True))
    op.add_column(
        "song", sa.Column("song_descriotion", sa.String(length=2000), nullable=True)
    )
    op.add_column(
        "song", sa.Column("ethnographic_district", sa.String(length=100), nullable=True)
    )
    op.add_column(
        "song", sa.Column("recording_location", sa.String(length=100), nullable=True)
    )
    op.add_column(
        "song", sa.Column("comment_map", sa.String(length=500), nullable=True)
    )
    op.add_column("song", sa.Column("video_url", sa.String(length=1000), nullable=True))
    op.add_column("song", sa.Column("photo1", sa.String(length=500), nullable=True))
    op.add_column("song", sa.Column("photo2", sa.String(length=500), nullable=True))
    op.add_column("song", sa.Column("photo3", sa.String(length=500), nullable=True))
    op.add_column(
        "song", sa.Column("stereo_audio", sa.String(length=1000), nullable=True)
    )
    op.add_column(
        "song", sa.Column("multichannel_audio1", sa.String(length=1000), nullable=True)
    )
    op.add_column(
        "song", sa.Column("multichannel_audio2", sa.String(length=1000), nullable=True)
    )
    op.add_column(
        "song", sa.Column("multichannel_audio3", sa.String(length=1000), nullable=True)
    )
    op.add_column(
        "song", sa.Column("multichannel_audio4", sa.String(length=1000), nullable=True)
    )
    op.add_column(
        "song", sa.Column("multichannel_audio5", sa.String(length=1000), nullable=True)
    )
    op.add_column(
        "song", sa.Column("multichannel_audio6", sa.String(length=1000), nullable=True)
    )
    op.add_column("song", sa.Column("city_id", sa.Integer(), nullable=True))
    op.create_foreign_key(None, "song", "cities", ["city_id"], ["id"])
    op.drop_column("song", "researcher_comment")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "song",
        sa.Column(
            "researcher_comment",
            sa.VARCHAR(length=1000),
            autoincrement=False,
            nullable=True,
        ),
    )
    op.drop_constraint(None, "song", type_="foreignkey")
    op.drop_column("song", "city_id")
    op.drop_column("song", "multichannel_audio6")
    op.drop_column("song", "multichannel_audio5")
    op.drop_column("song", "multichannel_audio4")
    op.drop_column("song", "multichannel_audio3")
    op.drop_column("song", "multichannel_audio2")
    op.drop_column("song", "multichannel_audio1")
    op.drop_column("song", "stereo_audio")
    op.drop_column("song", "photo3")
    op.drop_column("song", "photo2")
    op.drop_column("song", "photo1")
    op.drop_column("song", "video_url")
    op.drop_column("song", "comment_map")
    op.drop_column("song", "recording_location")
    op.drop_column("song", "ethnographic_district")
    op.drop_column("song", "song_descriotion")
    op.drop_column("song", "song_text")
    op.alter_column(
        "genre",
        "genre_name",
        existing_type=sa.String(length=100),
        type_=sa.VARCHAR(length=50),
        existing_nullable=True,
    )
    # ### end Alembic commands ###