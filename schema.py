from enum import Enum
from pydantic import BaseModel, field_validator
from datetime import date


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


class Album(BaseModel):
    title: str
    release_date: date


class BandBase(BaseModel):
    name: str
    genre: GenreChoices
    albums: list[Album] = []


class CreateBand(BandBase):
    @field_validator('genre', mode="before")
    def lower_case_genre(cls, value):
        return value.lower()

class BandWithId(BandBase):
    id: int
