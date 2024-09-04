from sqlmodel import Session, select
from fastapi import APIRouter, Depends, HTTPException
from app.models import Team 

router = APIRouter()

@router.post("/api/teams/", response_model=Team)
def create_team(team: Team, session: Session = Depends(get_session)):
    session.add(team)
    session.commit()
    session.refresh(team)
    return team

@router.get("/api/teams/", response_model=List[Team])
def read_teams(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    teams = session.exec(select(Team).offset(skip).limit(limit)).all()
    return teams

@router.get("/api/teams/{team_id}", response_model=Team)
def read_team(team_id: int, session: Session = Depends(get_session)):
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team

@router.put("/api/teams/{team_id}", response_model=Team)
def update_team(team_id: int, team: Team, session: Session = Depends(get_session)):
    db_team = session.get(Team, team_id)
    if not db_team:
        raise HTTPException(status_code=404, detail="Team not found")
    team_data = team.dict(exclude_unset=True)
    for key, value in team_data.items():
        setattr(db_team, key, value)
    session.add(db_team)
    session.commit()
    session.refresh(db_team)
    return db_team

@router.delete("/api/teams/{team_id}")
def delete_team(team_id: int, session: Session = Depends(get_session)):
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    session.delete(team)
    session.commit()
    return {"ok": True}
