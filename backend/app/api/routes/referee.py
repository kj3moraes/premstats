from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.core.db import get_session
from app.models import Referee

router = APIRouter()


# Referee CRUD operations
@router.post("/add", response_model=Referee, status_code=status.HTTP_201_CREATED)
def create_referee(referee: Referee, session: Session = Depends(get_session)):
    session.add(referee)
    session.commit()
    session.refresh(referee)
    return referee


@router.get("/list", response_model=List[Referee])
def read_referees(
    skip: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    referees = session.exec(select(Referee).offset(skip).limit(limit)).all()
    return referees


@router.get("/get/{referee_id}", response_model=Referee)
def read_referee(referee_id: int, session: Session = Depends(get_session)):
    referee = session.get(Referee, referee_id)
    if not referee:
        raise HTTPException(status_code=404, detail="Referee not found")
    return referee


@router.put("/update/{referee_id}", response_model=Referee)
def update_referee(
    referee_id: int, referee: Referee, session: Session = Depends(get_session)
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


@router.delete("/delete/{referee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_referee(referee_id: int, session: Session = Depends(get_session)):
    referee = session.get(Referee, referee_id)
    if not referee:
        raise HTTPException(status_code=404, detail="Referee not found")
    session.delete(referee)
    session.commit()
