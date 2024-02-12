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

__all__ = [
    AboutAdmin,
    OurTeamAdmin,
    FooterAdmin,
    PaymentAdmin,
    EducationAdmin,
    CountryAdmin,
    RegionAdmin,
    CityAdmin,
    SongAdmin,
    GenreAdmin,
    NewsCategoryAdmin,
    NewsAdmin,
    CalendarAndRitualCategoryAdmin,
    SongSubcategoryAdmin,
    EducationPageSongGenreAdmin,
]
