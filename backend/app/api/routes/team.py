from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.core.db import get_session
from app.models import Team

router = APIRouter()


@router.post("/add", response_model=Team, status_code=status.HTTP_201_CREATED)
def create_team(team: Team, session: Session = Depends(get_session)):
    session.add(team)
    session.commit()
    session.refresh(team)
    return team


@router.get("/list", response_model=List[Team])
def read_teams(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    teams = session.exec(select(Team).offset(skip).limit(limit)).all()
    return teams


@router.get("/get/{team_id}", response_model=Team)
def read_team(team_id: int, session: Session = Depends(get_session)):
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team


@router.put("/update/{team_id}", response_model=Team)
def update_team(team_id: int, team: Team, session: Session = Depends(get_session)):
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
