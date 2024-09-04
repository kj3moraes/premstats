from sqlmodel import Session, select
from fastapi import APIRouter, Depends, HTTPException
from app.models import Match 

router = APIRouter()

# Match CRUD operations
@router.post("/api/matches/", response_model=Match)
def create_match(match: Match, session: Session = Depends(get_session)):
    session.add(match)
    session.commit()
    session.refresh(match)
    return match

@router.get("/api/matches/", response_model=List[Match])
def read_matches(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    matches = session.exec(select(Match).offset(skip).limit(limit)).all()
    return matches

@router.get("/api/matches/{match_id}", response_model=Match)
def read_match(match_id: int, session: Session = Depends(get_session)):
    match = session.get(Match, match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    return match

@router.put("/api/matches/{match_id}", response_model=Match)
def update_match(match_id: int, match: Match, session: Session = Depends(get_session)):
    db_match = session.get(Match, match_id)
    if not db_match:
        raise HTTPException(status_code=404, detail="Match not found")
    match_data = match.dict(exclude_unset=True)
    for key, value in match_data.items():
        setattr(db_match, key, value)
    session.add(db_match)
    session.commit()
    session.refresh(db_match)
    return db_match

@router.delete("/api/matches/{match_id}")
def delete_match(match_id: int, session: Session = Depends(get_session)):
    match = session.get(Match, match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    session.delete(match)
    session.commit()
    return {"ok": True}