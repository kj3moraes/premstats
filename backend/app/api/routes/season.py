from typing import Annotated, List

from app.core.db import get_session
from app.core.security import verify_add_token, verify_delete_token, verify_update_token
from app.models import Season
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import AfterValidator
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

router = APIRouter()


@router.post(
    "/add",
    response_model=Season,
    status_code=status.HTTP_201_CREATED,
    include_in_schema=False,
)
def create_season(
    season: Annotated[Season, AfterValidator(Season.model_validate)],
    session: Session = Depends(get_session),
    token: str = Depends(verify_add_token),
):
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


@router.post(
    "/upsert",
    response_model=Season,
    status_code=status.HTTP_201_CREATED,
    include_in_schema=False,
)
def upsert_season(
    season: Annotated[Season, AfterValidator(Season.model_validate)],
    session: Session = Depends(get_session),
    token: str = Depends(verify_add_token),
):
    # Get the existing referee by the unique name
    statement = select(Season).where(Season.name == season.name)
    db_season = session.exec(statement).first()
    # If there is no season in the database then take the whole model
    if db_season is None:
        db_season = season
    else:
        # Otherwise, update the data (not the id)
        for key, value in season.model_dump(exclude={"id"}).items():
            setattr(db_season, key, value)

    session.add(db_season)
    session.commit()
    session.refresh(db_season)
    return db_season


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


@router.put("/update/{season_id}", response_model=Season, include_in_schema=False)
def update_season(
    season_id: int,
    season: Annotated[Season, AfterValidator(Season.model_validate)],
    session: Session = Depends(get_session),
    token: str = Depends(verify_update_token),
):
    db_season = session.get(Season, season_id)
    if not db_season:
        raise HTTPException(status_code=404, detail="Season not found")
    season_data = season.model_dump(exclude_unset=True)
    db_season.sqlmodel_update(season_data)
    session.add(db_season)
    session.commit()
    session.refresh(db_season)
    return db_season


@router.delete(
    "/delete/{season_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    include_in_schema=False,
)
def delete_season(
    season_id: int,
    session: Session = Depends(get_session),
    token: str = Depends(verify_delete_token),
):
    season = session.get(Season, season_id)
    if not season:
        raise HTTPException(status_code=404, detail="Season not found")
    session.delete(season)
    session.commit()
