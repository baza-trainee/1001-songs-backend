from sqlalchemy import Column, String, ForeignKey, Integer, Float
from sqlalchemy.orm import relationship

from src.database.database import Base


class Country(Base):
    __tablename__ = "countries"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

    regions = relationship("Region", back_populates="country", lazy="selectin")
    cities = relationship("City", back_populates="country")

    def __repr__(self) -> str:
        return f"{self.name}"


class Region(Base):
    __tablename__ = "regions"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    country_id = Column(Integer, ForeignKey("countries.id"))

    country = relationship("Country", back_populates="regions")
    cities = relationship("City", back_populates="region", lazy="selectin")

    def __repr__(self) -> str:
        return f"{self.name}"


class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    administrative_code = Column(String(50), nullable=False, unique=True)
    region_id = Column(Integer, ForeignKey("regions.id"))
    country_id = Column(Integer, ForeignKey("countries.id"))

    region = relationship(
        "Region",
        back_populates="cities",
        lazy="selectin",
    )
    country = relationship(
        "Country",
        back_populates="cities",
        lazy="selectin",
    )
    songs = relationship("Song", back_populates="city", lazy="selectin")
    expeditions = relationship("Expedition", back_populates="location", lazy="selectin")
    projects = relationship("OurProject", back_populates="location", lazy="selectin")
    news = relationship("News", back_populates="location", lazy="selectin")

    def __repr__(self) -> str:
        return f"{self.name}, {self.region}, {self.administrative_code}"
