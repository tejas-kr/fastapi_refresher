from typing import Union
from fastapi import FastAPI, HTTPException

app = FastAPI()

BANDS = [
    {'id': 1, 'name': 'AC/DC', 'genre': 'rock'},
    {'id': 2, 'name': 'the Beatles', 'genre': 'rock'},
    {'id': 3, 'name': 'the Judds', 'genre': 'country'},
    {'id': 4, 'name': 'Black Sabbath', 'genre': 'metal'},
]


@app.get("/bands")
async def get_all_bands() -> list[dict]:
    return BANDS


@app.get('/bands/{band_id}')
async def get_band(band_id: int) -> dict:
    band = next((b for b in BANDS if b['id'] == band_id), None)
    if not band:
        raise HTTPException(
            status_code=404,
            detail="Band Id not found"
        )
    return band
