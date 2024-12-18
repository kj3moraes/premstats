import json

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
        print("Failed to generate the SQL query.")
        raise HTTPException(
            status_code=400,
            detail=f"There currently is a problem with the service. Please try again later.",
        )

    # If the SQL query is invalid, return an error
    if sql_query.lower().strip() == "invalid":
        print("Failed to parse the question")
        raise HTTPException(
            status_code=400,
            detail=f"Sorry, I couldn't understand your question. Please try again.",
        )

    print(sql_query)
    try:
        # Execute the SQL query
        sql = text(sql_query)
        results = session.exec(sql).all()
    except Exception:
        raise HTTPException(
            status_code=400,
            detail=f"There currently is a problem with the service. Please try again later.",
        )

    # We need to do this because datetime objects need to converted into dictionaries
    data = [result._asdict() for result in results]
    answer_dicts = convert_rows_to_essentials(results)
    # If the answer dictionary is
    answer_dict_string = json.dumps(answer_dicts, default=str)
    if len(answer_dict_string) > 600:
        return {"message": "Click the button to get all the data.", "data": answer_dicts}

    answer = get_answer(user_question, answer_dicts)
    return {"message": answer, "data": data}
