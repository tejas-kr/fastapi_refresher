from enum import Enum
from datetime import date
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from pydantic import field_validator

# Pydantic Model classes are converted into SQLModels classes
# SQLModel class is a base class of pydantic BaseModel class


class GenreURLChoices(Enum):
    """
    Enum Class for Band Genres for URL
    """
    ROCK = 'rock'
    COUNTRY = 'country'
    METAL = 'metal'
    FOLK = 'folk'


class GenreChoices(Enum):
    """
    Enum Class for Band Genres for saving to DB
    """
    ROCK = 'rock'
    COUNTRY = 'country'
    METAL = 'metal'
    FOLK = 'folk'


class AlbumBase(SQLModel):
    """
    Album Base Model
    """
    title: str
    release_date: date
    band_id: int = Field(foreign_key="band.id", default=None)


class Album(AlbumBase, table=True):
    """
    Album Model. Table Schema
    """
    id: int = Field(default=None, primary_key=True)
    band: "Band" = Relationship(back_populates="albums")


class BandBase(SQLModel):
    """
    Band Base Model
    """
    name: str
    genre: GenreChoices


class BandCreate(BandBase):
    """
    Band Create Model
    """
    albums: Optional[list[AlbumBase]] = None

    @field_validator('genre', mode="before")
    def lower_case_genre(cls, value):
        return value.lower()


class Band(BandBase, table=True):
    """
    Band Model. Table Scheme
    """
    id: int = Field(default=None, primary_key=True)
    albums: list[Album] = Relationship(back_populates="band")
