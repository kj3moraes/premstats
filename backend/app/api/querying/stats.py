from app.api.querying.utils import (
    StatsRequest,
    convert_rows_to_essentials,
    get_answer,
    get_sql,
)
from app.core.db import get_session
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlmodel import Session

router = APIRouter()


@router.post("/ask_stats")
def get_stats(request: StatsRequest, session: Session = Depends(get_session)):
    user_question = request.message

    # Convert the natural language question to SQL
    try:
        sql_query = get_sql(user_question)
    except Exception:
        if sql_query == "Invalid":
            raise HTTPException(
                status_code=400,
                detail=f"Sorry, I couldn't understand your question. Please try again.",
            )
        else:
            raise HTTPException(
                status_code=400,
                detail=f"There currently is a problem with the service. Please try again later.",
            )

    try:
        # Execute the SQL query
        sql = text(sql_query)
        results = session.exec(sql).all()
    except Exception:
        raise HTTPException(
            status_code=400,
            detail=f"There currently is a problem with the service. Please try again later.",
        )

    data = [result._asdict() for result in results]
    answer_dicts = convert_rows_to_essentials(results)
    print(answer_dicts)
    answer = get_answer(user_question, answer_dicts)

    return {"message": answer, "data": data}
