from typing import Optional

from pydantic import BaseModel, Field

from .models import City


NAME_LEN = City.name.type.length


class BaseLocation(BaseModel):
    id: int = Field(..., ge=1)
    name: str = Field(..., max_length=NAME_LEN)


class RegionSchema(BaseLocation):
    country_id: int = Field(..., ge=1)


class CitySchema(BaseLocation):
    country_id: int = Field(..., ge=1)
    region_id: int = Field(..., ge=1)
    latitude: Optional[float] = Field(None, examples=[51.53694777241224])
    longitude: Optional[float] = Field(None, examples=[26.98664264])
