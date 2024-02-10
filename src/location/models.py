from sqlalchemy import Column, String, ForeignKey, Integer, Float
from sqlalchemy.orm import relationship
from src.database.database import Base


class Country(Base):
    __tablename__ = "countries"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

    regions = relationship("Region", back_populates="country")
    cities = relationship("City", back_populates="country")

    def __repr__(self) -> str:
        return f"{self.name}"


class Region(Base):
    __tablename__ = "regions"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    country_id = Column(Integer, ForeignKey("countries.id"))

    country = relationship("Country", back_populates="regions")
    cities = relationship("City", back_populates="region")

    def __repr__(self) -> str:
        return f"{self.name}"


class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    latitude = Column(Float)
    longitude = Column(Float)
    region_id = Column(Integer, ForeignKey("regions.id"))
    country_id = Column(Integer, ForeignKey("countries.id"))

    region = relationship("Region", back_populates="cities")
    country = relationship("Country", back_populates="cities")

    def __repr__(self) -> str:
        return f"{self.name}"
