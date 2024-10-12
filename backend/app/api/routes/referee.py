from typing import Annotated, List

from app.core.db import get_session
from app.core.security import verify_add_token, verify_delete_token, verify_update_token
from app.models import Referee, RefereeFilter
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_filter import FilterDepends
from pydantic import AfterValidator
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

router = APIRouter()


# Referee CRUD operations
@router.post(
    "/add",
    response_model=Referee,
    status_code=status.HTTP_201_CREATED,
    include_in_schema=False,
)
def create_referee(
    referee: Annotated[Referee, AfterValidator(Referee.model_validate)],
    session: Session = Depends(get_session),
    token: str = Depends(verify_add_token),
):
    referee = Referee.model_validate(referee)
    try:
        session.add(referee)
        session.commit()
        session.refresh(referee)
        return referee
    except IntegrityError as e:
        session.rollback()
        error_info = str(e.orig)
        if "ix_referee_name" in error_info:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Referee with name '{referee.name}' already exists.",
            )
        else:
            # If it's not a name conflict, re-raise the original exception
            raise e


@router.post(
    "/upsert",
    response_model=Referee,
    include_in_schema=False,
    status_code=status.HTTP_201_CREATED,
)
def upsert_referee(
    referee: Annotated[Referee, AfterValidator(Referee.model_validate)],
    session: Session = Depends(get_session),
    token: str = Depends(verify_add_token),
):

    # Get the existing referee by the unique name
    statement = select(Referee).where(Referee.name == referee.name)
    db_referee = session.exec(statement).first()
    # If there is no referee in the database then take the whole model
    if db_referee is None:
        db_referee = referee
    else:
        # Otherwise, update the data (not the id)
        for key, value in referee.model_dump(exclude={"id"}).items():
            setattr(db_referee, key, value)

    session.add(db_referee)
    session.commit()
    session.refresh(db_referee)
    return db_referee


@router.get("/list", response_model=List[Referee])
def read_referees(
    referee_filter: RefereeFilter = FilterDepends(RefereeFilter),
    session: Session = Depends(get_session),
):
    query = select(Referee)
    query = referee_filter.filter(query)
    query = referee_filter.sort(query)
    referees = session.exec(query).all()
    return referees


@router.get("/get/{referee_id}", response_model=Referee)
def read_referee(referee_id: int, session: Session = Depends(get_session)):
    referee = session.get(Referee, referee_id)
    if not referee:
        raise HTTPException(status_code=404, detail="Referee not found")
    return referee


@router.put("/update/{referee_id}", response_model=Referee, include_in_schema=False)
def update_referee(
    referee_id: int,
    referee: Annotated[Referee, AfterValidator(Referee.model_validate)],
    session: Session = Depends(get_session),
    token: str = Depends(verify_update_token),
):
    db_referee = session.get(Referee, referee_id)
    if not db_referee:
        raise HTTPException(status_code=404, detail="Referee not found")
    referee_data = referee.model_dump(exclude_unset=True)
    db_referee.sqlmodel_update(referee_data)
    session.add(db_referee)
    session.commit()
    session.refresh(db_referee)
    return db_referee


@router.delete(
    "/delete/{referee_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    include_in_schema=False,
)
def delete_referee(
    referee_id: int,
    session: Session = Depends(get_session),
    token: str = Depends(verify_delete_token),
):
    referee = session.get(Referee, referee_id)
    if not referee:
        raise HTTPException(status_code=404, detail="Referee not found")
    session.delete(referee)
    session.commit()
