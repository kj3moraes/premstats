from typing import Annotated, List

from app.core.db import get_session
from app.core.security import verify_token
from app.models import Referee
from fastapi import APIRouter, Depends, HTTPException, status
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


@router.get("/list", response_model=List[Referee])
def read_referees(session: Session = Depends(get_session)):
    referees = session.exec(select(Referee)).all()
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
):
    db_referee = session.get(Referee, referee_id)
    if not db_referee:
        raise HTTPException(status_code=404, detail="Referee not found")
    referee_data = referee.model_dump(exclude_unset=True)
    for key, value in referee_data.items():
        setattr(db_referee, key, value)
    session.add(db_referee)
    session.commit()
    session.refresh(db_referee)
    return db_referee


@router.delete(
    "/delete/{referee_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    include_in_schema=False,
)
def delete_referee(referee_id: int, session: Session = Depends(get_session)):
    referee = session.get(Referee, referee_id)
    if not referee:
        raise HTTPException(status_code=404, detail="Referee not found")
    session.delete(referee)
    session.commit()
