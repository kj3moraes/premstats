from sqlmodel import Session, select
from fastapi import APIRouter, Depends, HTTPException
from app.models import Season

router = APIRouter()

@router.post("/add", response_model=Season)
def create_season(season: Season, session: Session = Depends(get_session)):
    session.add(season)
    session.commit()
    session.refresh(season)
    return season

@router.get("/list", response_model=List[Season])
def read_seasons(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    seasons = session.exec(select(Season).offset(skip).limit(limit)).all()
    return seasons

@router.get("/get/{season_id}", response_model=Season)
def read_season(season_id: int, session: Session = Depends(get_session)):
    season = session.get(Season, season_id)
    if not season:
        raise HTTPException(status_code=404, detail="Season not found")
    return season

@router.put("/update/{season_id}", response_model=Season)
def update_season(season_id: int, season: Season, session: Session = Depends(get_session)):
    db_season = session.get(Season, season_id)
    if not db_season:
        raise HTTPException(status_code=404, detail="Season not found")
    season_data = season.dict(exclude_unset=True)
    for key, value in season_data.items():
        setattr(db_season, key, value)
    session.add(db_season)
    session.commit()
    session.refresh(db_season)
    return db_season

@router.delete("/delete/{season_id}")
def delete_season(season_id: int, session: Session = Depends(get_session)):
    season = session.get(Season, season_id)
    if not season:
        raise HTTPException(status_code=404, detail="Season not found")
    session.delete(season)
    session.commit()
    return {"ok": True}