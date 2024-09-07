from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlmodel import Session, select
from app.core.db import get_session
from app.models import Match

router = APIRouter()

# Match CRUD operations
@router.post("/add", response_model=Match, status_code=status.HTTP_201_CREATED)
def create_match(match: Match, session: Session = Depends(get_session)):
    session.add(match)
    session.commit()
    session.refresh(match)
    return match 


@router.get("/list", response_model=List[Match])
def read_matches(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    matches = session.exec(select(Match).offset(skip).limit(limit)).all()
    return matches


@router.get("/get/{match_id}", response_model=Match)
def read_match(match_id: int, session: Session = Depends(get_session)):
    match = session.get(Match, match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    return match


@router.put("/update/{match_id}", response_model=Match)
def update_match(match_id: int, match: Match, session: Session = Depends(get_session)):
    db_match = session.get(Match, match_id)
    if not db_match:
        raise HTTPException(status_code=404, detail="Match not found")
    match_data = match.model_dump(exclude_unset=True)
    for key, value in match_data.items():
        setattr(db_match, key, value)
    session.add(db_match)
    session.commit()
    session.refresh(db_match)
    return db_match


@router.delete("/delete/{match_id}")
def delete_match(match_id: int, session: Session = Depends(get_session)):
    match = session.get(Match, match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    session.delete(match)
    session.commit()
