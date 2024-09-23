from fastapi import FastAPI, HTTPException, Path, Query, Depends
from sqlmodel import Session, select
from contextlib import asynccontextmanager
from typing import Optional, Annotated
from models import (
    GenreURLChoices, BandBase, BandCreate, Band, Album
)
from db import init_db, get_session


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)


@app.get("/bands")
async def get_all_bands(
    genre: Optional[GenreURLChoices] = None,
    q: Annotated[Optional[str], Query(max_length=10)] = None,
    session: Session = Depends(get_session)
) -> list[Band]:
    bands = session.exec(select(Band)).all()
    print("all bands:", bands)
    if genre:
        bands = [b for b in bands if b.genre.value == genre.value.lower()]
    if q:
        bands = [b for b in bands if q.lower() in b.name.lower()]
    return bands


@app.get('/bands/{band_id}')
async def get_band(
    band_id: Annotated[int, Path(title="The band Id")],
    session: Session = Depends(get_session)
) -> Band:
    band: Band = session.get(Band, band_id)
    print("band details:", band)
    if not band:
        raise HTTPException(
            status_code=404,
            detail="Band Id not found"
        )
    return band


@app.post('/bands')
async def create_band(
    band_data: BandCreate,
    session: Session = Depends(get_session)
) -> Band:
    band = Band(name=band_data.name, genre=band_data.genre)
    session.add(band)

    if band_data.albums:
        for album in band_data.albums:
            album_obj = Album(title=album.title, release_date=album.release_date, band=band)
            session.add(album_obj)

    session.commit()
    session.refresh(band)

    return band
