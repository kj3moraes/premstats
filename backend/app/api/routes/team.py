from typing import Annotated, List

from app.core.db import get_session
from app.core.security import verify_add_token, verify_delete_token, verify_update_token
from app.models import Team, TeamFilter, TeamSeason, TeamSeasonFilter
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_filter import FilterDepends
from pydantic import AfterValidator
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

router = APIRouter()


@router.post(
    "/add",
    response_model=Team,
    status_code=status.HTTP_201_CREATED,
    include_in_schema=False,
)
def create_team(
    team: Annotated[Team, AfterValidator(Team.model_validate)],
    session: Session = Depends(get_session),
    token: str = Depends(verify_add_token),
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


@router.post(
    "/upsert",
    response_model=Team,
    include_in_schema=False,
    status_code=status.HTTP_201_CREATED,
)
def upsert_team(
    team: Annotated[Team, AfterValidator(Team.model_validate)],
    session: Session = Depends(get_session),
    token: str = Depends(verify_add_token),
):
    # Get the existing referee by the unique name
    statement = select(Team).where(Team.name == team.name)
    db_team = session.exec(statement).first()
    # If there is no team in the database then take the whole model
    if db_team is None:
        db_team = team
    else:
        # Otherwise, update the data (not the id)
        for key, value in team.model_dump(exclude={"id"}).items():
            setattr(db_team, key, value)

    session.add(db_team)
    session.commit()
    session.refresh(db_team)
    return db_team


@router.get("/list", response_model=List[Team])
def read_referees(
    team_filter: TeamFilter = FilterDepends(TeamFilter),
    session: Session = Depends(get_session),
):
    query = select(Team)
    query = team_filter.filter(query)
    query = team_filter.sort(query)
    referees = session.exec(query).all()
    return referees


@router.get("/get/{team_id}", response_model=Team)
def read_team(team_id: int, session: Session = Depends(get_session)):
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team


@router.put("/update/{team_id}", response_model=Team, include_in_schema=False)
def update_team(
    team_id: int,
    team: Annotated[Team, AfterValidator(Team.model_validate)],
    session: Session = Depends(get_session),
    token: str = Depends(verify_update_token),
):
    db_team = session.get(Team, team_id)
    if not db_team:
        raise HTTPException(status_code=404, detail="Team not found")
    team_data = team.model_dump(exclude_unset=True)
    db_team.sqlmodel_update(team_data)
    session.add(db_team)
    session.commit()
    session.refresh(db_team)
    return db_team


@router.delete(
    "/delete/{team_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    include_in_schema=False,
)
def delete_team(
    team_id: int,
    session: Session = Depends(get_session),
    token: str = Depends(verify_delete_token),
):
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    session.delete(team)
    session.commit()


@router.post(
    "/season/upsert",
    response_model=TeamSeason,
    include_in_schema=False,
    status_code=status.HTTP_201_CREATED,
)
def upsert_team_season(
    team_season: Annotated[TeamSeason, AfterValidator(TeamSeason.model_validate)],
    session: Session = Depends(get_session),
    token: str = Depends(verify_add_token),
):
    # Get the existing team_season by the unique combination of team_id and season_id
    statement = select(TeamSeason).where(
        TeamSeason.team_name == team_season.team_name,
        TeamSeason.season_name == team_season.season_name,
    )
    db_team_season = session.exec(statement).first()

    # If there is no team_season in the database then take the whole model
    if db_team_season is None:
        db_team_season = team_season
    else:
        # Otherwise, update the data (not the id)
        for key, value in team_season.model_dump(exclude={"id"}).items():
            setattr(db_team_season, key, value)

    session.add(db_team_season)
    session.commit()
    session.refresh(db_team_season)
    return db_team_season


@router.get("/season/list", response_model=List[TeamSeason])
def read_team_seasons(
    skip: int = 0,
    limit: int = 100,
    team_season_filter: TeamSeason = FilterDepends(TeamSeasonFilter),
    session: Session = Depends(get_session),
):
    query = select(TeamSeason)
    query = team_season_filter.filter(query)
    query = team_season_filter.sort(query)
    team_seasons = session.exec(query.offset(skip).limit(limit)).all()
    return team_seasons
