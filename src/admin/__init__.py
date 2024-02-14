from .payment import PaymentAdmin
from .our_team import OurTeamAdmin
from .footer import FooterAdmin

from .education import (
    EducationAdmin,
    CalendarAndRitualCategoryAdmin,
    SongSubcategoryAdmin,
    EducationPageSongGenreAdmin,
)
from .about import AboutAdmin
from .location import CountryAdmin, RegionAdmin, CityAdmin
from .song import SongAdmin, GenreAdmin
from .news import NewsAdmin, NewsCategoryAdmin
from .expedition import ExpeditionAdmin

__all__ = [
    NewsCategoryAdmin,
    NewsAdmin,
    RegionAdmin,
    EducationAdmin,
    CountryAdmin,
    CityAdmin,
    GenreAdmin,
    SongAdmin,
    CalendarAndRitualCategoryAdmin,
    SongSubcategoryAdmin,
    EducationPageSongGenreAdmin,
    AboutAdmin,
    OurTeamAdmin,
    ExpeditionAdmin,
    FooterAdmin,
    PaymentAdmin,
]
