from typing import Annotated, List

from app.core.db import get_session
from app.models import Team
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import AfterValidator
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

router = APIRouter()


@router.post("/add", response_model=Team, status_code=status.HTTP_201_CREATED)
def create_team(
    team: Annotated[Team, AfterValidator(Team.model_validate)],
    session: Session = Depends(get_session),
):
    try:
        session.add(team)
        session.commit()
        session.refresh(team)
        return team
    except IntegrityError as e:
        session.rollback()
        error_info = str(e.orig)
        if "ix_team_name" in error_info:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Team with name '{team.name}' already exists.",
            )
        else:
            # If it's not a name conflict, re-raise the original exception
            raise e


@router.get("/list", response_model=List[Team])
def read_teams(session: Session = Depends(get_session)):
    teams = session.exec(select(Team)).all()
    return teams


@router.get("/get/{team_id}", response_model=Team)
def read_team(team_id: int, session: Session = Depends(get_session)):
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team


@router.put("/update/{team_id}", response_model=Team)
def update_team(
    team_id: int,
    team: Annotated[Team, AfterValidator(Team.model_validate)],
    session: Session = Depends(get_session),
):
    db_team = session.get(Team, team_id)
    if not db_team:
        raise HTTPException(status_code=404, detail="Team not found")
    team_data = team.model_dump(exclude_unset=True)
    for key, value in team_data.items():
        setattr(db_team, key, value)
    session.add(db_team)
    session.commit()
    session.refresh(db_team)
    return db_team


@router.delete("/delete/{team_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_team(team_id: int, session: Session = Depends(get_session)):
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    session.delete(team)
    session.commit()
