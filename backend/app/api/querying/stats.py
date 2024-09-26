from datetime import datetime

from app.api.querying.utils import PROMPT, StatsRequest, get_sql
from app.core.db import get_session
from app.models import Match
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlmodel import Session, select

router = APIRouter()


@router.post("/ask_stats")
def get_stats(request: StatsRequest, session: Session = Depends(get_session)):
    user_question = request.message

    # Convert the natural language question to SQL
    sql_query = get_sql(user_question)

    print(sql_query)
    sql = text(sql_query)

    # Execute the SQL query
    try:
        result = session.exec(sql).all()
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"There currently is a problem with the service. Please try again. {str(e)}",
        )
    print(result)

    return {"message": "Success"}
