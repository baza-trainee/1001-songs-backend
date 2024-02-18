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
from .song import SongAdmin, GenreAdmin, FundAdmin
from .news import NewsAdmin
from .expedition import ExpeditionAdmin
from .project import OurProjectAdmin
from .pass_change import ChangePasswordAdmin, PasswordRecoveryAdmin

__all__ = [
    CountryAdmin,
    RegionAdmin,
    CityAdmin,
    EducationAdmin,
    GenreAdmin,
    SongAdmin,
    CalendarAndRitualCategoryAdmin,
    SongSubcategoryAdmin,
    EducationPageSongGenreAdmin,
    AboutAdmin,
    OurTeamAdmin,
    NewsAdmin,
    ExpeditionAdmin,
    OurProjectAdmin,
    FooterAdmin,
    PaymentAdmin,
    FundAdmin,
    ChangePasswordAdmin,
    PasswordRecoveryAdmin,
]
