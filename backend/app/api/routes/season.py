from typing import List

from app.core.db import get_session
from app.models import Season
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

router = APIRouter()


@router.post("/add", response_model=Season, status_code=status.HTTP_201_CREATED)
def create_season(season: Season, session: Session = Depends(get_session)):
    try:
        session.add(season)
        session.commit()
        session.refresh(season)
        return season
    except IntegrityError as e:
        session.rollback()
        error_info = str(e.orig)
        if "ix_season_name" in error_info:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Season with name '{season.name}' already exists.",
            )
        else:
            # If it's not a name conflict, re-raise the original exception
            raise e


@router.get("/list", response_model=List[Season])
def read_seasons(session: Session = Depends(get_session)):
    seasons = session.exec(select(Season)).all()
    return seasons


@router.get("/get/{season_id}", response_model=Season)
def read_season(season_id: int, session: Session = Depends(get_session)):
    season = session.get(Season, season_id)
    if not season:
        raise HTTPException(status_code=404, detail="Season not found")
    return season


@router.put("/update/{season_id}", response_model=Season)
def update_season(
    season_id: int, season: Season, session: Session = Depends(get_session)
):
    db_season = session.get(Season, season_id)
    if not db_season:
        raise HTTPException(status_code=404, detail="Season not found")
    season_data = season.model_dump(exclude_unset=True)
    for key, value in season_data.items():
        setattr(db_season, key, value)
    session.add(db_season)
    session.commit()
    session.refresh(db_season)
    return db_season


@router.delete("/delete/{season_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_season(season_id: int, session: Session = Depends(get_session)):
    season = session.get(Season, season_id)
    if not season:
        raise HTTPException(status_code=404, detail="Season not found")
    session.delete(season)
    session.commit()
