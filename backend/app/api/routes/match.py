from datetime import date
from typing import Annotated, List

from app.core.db import get_session
from app.core.security import verify_add_token, verify_delete_token, verify_update_token
from app.models import Match
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import AfterValidator, ValidationError
from sqlmodel import Session, select

router = APIRouter()


# Match CRUD operations
@router.post(
    "/add",
    response_model=Match,
    status_code=status.HTTP_201_CREATED,
    include_in_schema=False,
)
def create_match(
    match: Match,
    session: Session = Depends(get_session),
    token: str = Depends(verify_add_token),
):
    session.add(match)
    session.commit()
    session.refresh(match)
    return match


@router.post(
    "/upsert",
    response_model=Match,
    include_in_schema=False,
    status_code=status.HTTP_201_CREATED,
)
def upsert_match(
    match: Match,
    session: Session = Depends(get_session),
    token: str = Depends(verify_add_token),
):
    # Get the existing match by season, home_team_name, away_team_name, and match_date
    date_parsed = date.fromisoformat(match.match_date)
    statement = select(Match).where(
        Match.season_name == match.season_name,
        Match.home_team_name == match.home_team_name,
        Match.away_team_name == match.away_team_name,
        Match.match_date == date_parsed,
    )
    db_match = session.exec(statement).first()

    if db_match is None:
        db_match = match
    else:
        # Otherwise, update the data (not the id)
        try:
            match = Match.model_validate(match)
        except ValidationError:
            raise HTTPException(status_code=400, detail="Invalid match data")
        for key, value in match.model_dump(exclude={"id"}).items():
            setattr(db_match, key, value)

    session.add(db_match)
    session.commit()
    session.refresh(db_match)
    return db_match


@router.get("/list", response_model=List[Match])
def read_matches(
    skip: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    matches = session.exec(select(Match).offset(skip).limit(limit)).all()
    return matches


@router.get("/get/{match_id}", response_model=Match)
def read_match(match_id: int, session: Session = Depends(get_session)):
    match = session.get(Match, match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    return match


@router.put("/update/{match_id}", response_model=Match, include_in_schema=False)
def update_match(
    match_id: int,
    match: Annotated[Match, AfterValidator(Match.model_validate)],
    session: Session = Depends(get_session),
    token: str = Depends(verify_update_token),
):
    db_match = session.get(Match, match_id)
    if not db_match:
        raise HTTPException(status_code=404, detail="Match not found")
    match_data = match.model_dump(exclude_unset=True)
    db_match.sqlmodel_update(match_data)
    session.add(db_match)
    session.commit()
    session.refresh(db_match)
    return db_match


@router.delete(
    "/delete/{match_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    include_in_schema=False,
)
def delete_match(
    match_id: int,
    session: Session = Depends(get_session),
    token: str = Depends(verify_delete_token),
):
    match = session.get(Match, match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    session.delete(match)
    session.commit()
