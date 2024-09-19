from typing import Annotated, List

from app.core.db import get_session
from app.models import Season
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import AfterValidator
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

router = APIRouter()


@router.post("/ask_stats")
def get_stats():
    return {"message": "Hello World"}
