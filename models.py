from enum import Enum
from datetime import date
from typing import Union, Optional
from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel, field_validator

# Pydantic Model classes are converted into SQLModels classes
# SQLModel class is a base class of pydantic BaseModel class


class GenreURLChoices(Enum):
    ROCK = 'rock'
    COUNTRY = 'country'
    METAL = 'metal'
    FOLK = 'folk'


class GenreChoices(Enum):
    ROCK = 'rock'
    COUNTRY = 'country'
    METAL = 'metal'
    FOLK = 'folk'


class AlbumBase(SQLModel):
    title: str
    release_date: date
    band_id: int = Field(foreign_key="band.id", default=None)


class Album(AlbumBase, table=True):
    id: int = Field(default=None, primary_key=True)
    band: "Band" = Relationship(back_populates="albums")


class BandBase(SQLModel):
    name: str
    genre: GenreChoices


class BandCreate(BandBase):
    albums: Optional[list[AlbumBase]] = None

    @field_validator('genre', mode="before")
    def lower_case_genre(cls, value):
        return value.lower()


class Band(BandBase, table=True):
    id: int = Field(default=None, primary_key=True)
    albums: list[Album] = Relationship(back_populates="band")
