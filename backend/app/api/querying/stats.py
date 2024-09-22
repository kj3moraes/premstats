from datetime import datetime
from typing import Annotated, List

import requests
from app.api.querying.utils import PROMPT, StatsRequest, query
from app.core.db import get_session
from app.models import Match
from fastapi import APIRouter
from sqlmodel import Session, select

router = APIRouter()


@router.post("/ask_stats")
def get_stats(request: StatsRequest):
    user_question = request.message

    # Populate the prompt with the user question
    prompt = PROMPT.format(
        user_question=user_question, current_date=datetime.now().strftime("%Y-%m-%d")
    )
    response = query({"inputs": prompt})
    return {"message": response}
