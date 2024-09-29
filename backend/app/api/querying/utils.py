from datetime import datetime
from typing import List

import requests
from app.core.config import settings
from fastapi import HTTPException
from groq import Groq
from pydantic import BaseModel
from sqlalchemy import Row

# The following prompt has 2 variables:
# - user_question: str
# - current_date: str
SQL_BOT_SYSTEM_PROMPT = """
You are a Natural language to SQL bot for a database of Premier League Matches.
You must only output a single SQL query to answer the user's question.

Instructions:
- if the question cannot be answered given the database schema, return "invalid"
- if the question is invalid, return "invalid"
- first season of the premier league in our database was 1993/94
- ignore "division" in the schema
- the "prem" is short for the Premier League
- Use the full names of teams (Man United is Manchester United, etc.)
- recall that the current date in YYYY-MM-DD format is {current_date} 
- when asked for a season, you must query season_name with "English Premier League YYYY/YY Season" format
- full_time_result is either "H" (home win), "A" (away win), or "D" (draw)
- half_time_result is either "H" (home win), "A" (away win), or "D" (draw)

The schema is: 
CREATE TABLE public.referee (
	id serial4 NOT NULL,
	"name" varchar NOT NULL,
	CONSTRAINT referee_pkey PRIMARY KEY (id)
);

CREATE TABLE public.season (
	id serial4 NOT NULL,
	"name" varchar NOT NULL,
	CONSTRAINT season_pkey PRIMARY KEY (id)
);

CREATE TABLE public.team (
	id serial4 NOT NULL,
	"name" varchar NOT NULL,
	CONSTRAINT team_pkey PRIMARY KEY (id)
);

CREATE TABLE public."match" (
	id serial4 NOT NULL,
	season_name varchar NOT NULL,
	division varchar NOT NULL,
	match_date date NOT NULL,
	match_time time NULL,
	home_team_name varchar NOT NULL,
	away_team_name varchar NOT NULL,
	referee_name varchar NULL,
	full_time_home_goals int4 NOT NULL,
	full_time_away_goals int4 NOT NULL,
	full_time_result varchar NOT NULL,
	half_time_home_goals int4 NULL,
	half_time_away_goals int4 NULL,
	half_time_result varchar NULL,
	home_shots int4 NULL,
	away_shots int4 NULL,
	home_shots_on_target int4 NULL,
	away_shots_on_target int4 NULL,
	home_fouls int4 NULL,
	away_fouls int4 NULL,
	home_corners int4 NULL,
	away_corners int4 NULL,
	home_yellow_cards int4 NULL,
	away_yellow_cards int4 NULL,
	home_red_cards int4 NULL,
	away_red_cards int4 NULL,
	bet365_home_win_odds float8 NULL,
	bet365_draw_odds float8 NULL,
	bet365_away_win_odds float8 NULL,
	bet_and_win_home_win_odds float8 NULL,
	bet_and_win_draw_odds float8 NULL,
	bet_and_win_away_win_odds float8 NULL,
	interwetten_home_win_odds float8 NULL,
	interwetten_draw_odds float8 NULL,
	interwetten_away_win_odds float8 NULL,
	pinnacle_home_win_odds float8 NULL,
	pinnacle_draw_odds float8 NULL,
	pinnacle_away_win_odds float8 NULL,
	william_hill_home_win_odds float8 NULL,
	william_hill_draw_odds float8 NULL,
	william_hill_away_win_odds float8 NULL,
	vc_bet_home_win_odds float8 NULL,
	vc_bet_draw_odds float8 NULL,
	vc_bet_away_win_odds float8 NULL,
	max_home_win_odds float8 NULL,
	max_draw_odds float8 NULL,
	max_away_win_odds float8 NULL,
	avg_home_win_odds float8 NULL,
	avg_draw_odds float8 NULL,
	avg_away_win_odds float8 NULL,
	bet365_over_2_5_odds float8 NULL,
	bet365_under_2_5_odds float8 NULL,
	pinnacle_over_2_5_odds float8 NULL,
	pinnacle_under_2_5_odds float8 NULL,
	max_over_2_5_odds float8 NULL,
	max_under_2_5_odds float8 NULL,
	avg_over_2_5_odds float8 NULL,
	avg_under_2_5_odds float8 NULL,
	CONSTRAINT match_pkey PRIMARY KEY (id),
	CONSTRAINT match_away_team_name_fkey FOREIGN KEY (away_team_name) REFERENCES public.team("name"),
	CONSTRAINT match_home_team_name_fkey FOREIGN KEY (home_team_name) REFERENCES public.team("name"),
	CONSTRAINT match_referee_name_fkey FOREIGN KEY (referee_name) REFERENCES public.referee("name"),
	CONSTRAINT match_season_name_fkey FOREIGN KEY (season_name) REFERENCES public.season("name")
);

```sql
"""


ANSWER_BOT_SYSTEM_PROMPT = """
You are a question answer bot. The user will provide some dictionaries with match data and their original question. 
You task is to frame an answer that is relevant to the question and the data provided.
"""

ANSWER_BOT_USER_PROMPT = """
This is the original question {user_question}
And this is the query result {match_data}.

Frame an answer out of these.
"""


class StatsRequest(BaseModel):
    message: str


client = Groq(
    api_key=settings.GROQ_API_KEY,
)


def get_sql(query: str):
    chat_completions = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": SQL_BOT_SYSTEM_PROMPT.format(
                    current_date=datetime.now().strftime("%Y-%m-%d")
                ),
            },
            {"role": "user", "content": query},
        ],
        model="llama-3.1-70b-versatile",
    )

    sql = chat_completions.choices[0].message.content
    sql = sql.replace("```sql", "")
    sql = sql.replace("```", " ")
    return sql


def get_answer(user_question: str, data):
    prompt = ANSWER_BOT_USER_PROMPT.format(user_question=user_question, match_data=data)
    try:
        chat_completions = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": ANSWER_BOT_SYSTEM_PROMPT,
                },
                {"role": "user", "content": prompt},
            ],
            model="llama-3.1-70b-versatile",
        )

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"There currently is a problem with the service. Please try again.",
        )

    response = chat_completions.choices[0].message.content
    return response


def convert_rows_to_essentials(results: List[Row]):
    dicts = [row._asdict() for row in results]

    # Remove None values and odds information
    for d in dicts:
        for k, v in list(d.items()):
            if v is None or "odds" in k:
                del d[k]
    return dicts
