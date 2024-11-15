from typing import Annotated, List

from app.core.db import get_session
from app.core.security import verify_add_token, verify_delete_token, verify_update_token
from app.models import Stadium, StadiumFilter, Team
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_filter import FilterDepends
from pydantic import AfterValidator
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

router = APIRouter()


# Stadium CRUD operations
@router.post(
    "/add",
    response_model=Stadium,
    status_code=status.HTTP_201_CREATED,
    include_in_schema=False,
)
def create_stadium(
    stadium: Annotated[Stadium, AfterValidator(Stadium.model_validate)],
    session: Session = Depends(get_session),
    token: str = Depends(verify_add_token),
):
    stadium = Stadium.model_validate(stadium)
    try:
        # Check if the team exists first
        team_statement = select(Team).where(Team.name == stadium.home_team)
        team = session.exec(team_statement).first()
        if not team:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Team '{stadium.home_team}' does not exist.",
            )

        session.add(stadium)
        session.commit()
        session.refresh(stadium)
        return stadium
    except IntegrityError as e:
        session.rollback()
        error_info = str(e.orig)
        if "stadium_pkey" in error_info:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Stadium with name '{stadium.name}' already exists.",
            )
        else:
            # If it's not a name conflict, re-raise the original exception
            raise e


@router.post(
    "/upsert",
    response_model=Stadium,
    include_in_schema=False,
    status_code=status.HTTP_201_CREATED,
)
def upsert_stadium(
    stadium: Stadium,
    session: Session = Depends(get_session),
    token: str = Depends(verify_add_token),
):

    # Get the existing Stadium by the unique name
    statement = select(Stadium).where(Stadium.name == stadium.name)
    db_stadium = session.exec(statement).first()
    # If there is no Stadium in the database then take the whole model
    if db_stadium is None:
        db_stadium = stadium
    else:
        # Otherwise, update the data (not the id)
        for key, value in stadium.model_dump(exclude={"id"}).items():
            setattr(db_stadium, key, value)

    session.add(db_stadium)
    session.commit()
    session.refresh(db_stadium)
    return db_stadium


@router.get("/list", response_model=List[Stadium])
def read_stadiums(
    stadium_filter: StadiumFilter = FilterDepends(StadiumFilter),
    session: Session = Depends(get_session),
):
    query = select(Stadium)
    query = stadium_filter.filter(query)
    query = stadium_filter.sort(query)
    stadiums = session.exec(query).all()
    return stadiums


@router.get("/get/{stadium_id}", response_model=Stadium)
def read_stadium(stadium_id: int, session: Session = Depends(get_session)):
    stadium = session.get(Stadium, stadium_id)
    if not stadium:
        raise HTTPException(status_code=404, detail="Stadium not found")
    return stadium


@router.put("/update/{stadium_id}", response_model=Stadium, include_in_schema=False)
def update_stadium(
    stadium_id: int,
    stadium: Annotated[Stadium, AfterValidator(Stadium.model_validate)],
    session: Session = Depends(get_session),
    token: str = Depends(verify_update_token),
):
    db_stadium = session.get(Stadium, stadium_id)
    if not db_stadium:
        raise HTTPException(status_code=404, detail="Stadium not found")
    stadium_data = stadium.model_dump(exclude_unset=True)
    db_stadium.sqlmodel_update(stadium_data)
    session.add(db_stadium)
    session.commit()
    session.refresh(db_stadium)
    return db_stadium


@router.delete(
    "/delete/{stadium_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    include_in_schema=False,
)
def delete_Stadium(
    stadium_id: int,
    session: Session = Depends(get_session),
    token: str = Depends(verify_delete_token),
):
    stadium = session.get(Stadium, stadium_id)
    if not stadium:
        raise HTTPException(status_code=404, detail="Stadium not found")
    session.delete(stadium)
    session.commit()
