from fastapi import FastAPI, HTTPException, Path, Query
from typing import Optional, Annotated
from schema import (
    GenreURLChoices, BandBase, CreateBand, BandWithId,
)

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
    q: Annotated[Optional[str], Query(max_length=10)] = None
) -> list[BandBase]:
    bands = [BandBase(**b) for b in BANDS]
    if genre:
        bands = [b for b in bands if b.genre.value == genre.value.lower()]
    if q:
        bands = [b for b in bands if q.lower() in b.name.lower()]
    return bands


@app.get('/bands/{band_id}')
async def get_band(band_id: Annotated[int, Path(description="The band Id")]) -> BandBase:
    band = next((BandBase(**b) for b in BANDS if b['id'] == band_id), None)
    if not band:
        raise HTTPException(
            status_code=404,
            detail="Band Id not found"
        )
    return band


@app.post('/bands')
async def create_band(band_data: CreateBand) -> BandWithId:
    id = BANDS[-1]['id'] + 1
    band = BandWithId(id=id, **band_data.model_dump()).model_dump()
    BANDS.append(band)
    return BandWithId(**band)
