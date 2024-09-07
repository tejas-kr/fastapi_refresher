from schema import GenreURLChoices, Band
from fastapi import FastAPI, HTTPException
from typing import Optional

app = FastAPI()


BANDS = [
    {'id': 1, 'name': 'AC/DC', 'genre': 'rock'},
    {'id': 2, 'name': 'the Beatles', 'genre': 'rock', 'albums': [
        {'title': 'Please Please Me', 'release_date': '1963-03-22'}
    ]},
    {'id': 3, 'name': 'the Judds', 'genre': 'country'},
    {'id': 4, 'name': 'Black Sabbath', 'genre': 'metal', 'albums': [
        {'title': 'paranoid', 'release_date': '1970-09-18'}
    ]},
]


@app.get("/bands")
async def get_all_bands(
    genre: Optional[GenreURLChoices] = None,
    has_albums: bool = True
) -> list[Band]:
    bands = [Band(**b) for b in BANDS]
    if genre:
        bands = [b for b in bands if b.genre.lower() == genre.value.lower()]
    if has_albums:
        bands = [b for b in bands if len(b.albums) > 0]
    else:
        bands = [b for b in bands if len(b.albums) == 0]
    return bands


@app.get('/bands/{band_id}')
async def get_band(band_id: int) -> Band:
    band = next((Band(**b) for b in BANDS if b['id'] == band_id), None)
    if not band:
        raise HTTPException(
            status_code=404,
            detail="Band Id not found"
        )
    return band
