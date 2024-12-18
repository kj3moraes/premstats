import os
from datetime import datetime
from typing import List

from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import Row
from together import Together

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
- when using teamseason, use quotes for the "t1.name"
- the "prem" is short for the Premier League
- remeber to bracket correctly for AND/OR operations
- Use the full names of teams (Man United is Manchester United, etc.)
- if teams ask for QPR, use "QPR" not "Queens Park Rangers". If they ask for "Hull" use "Hull" itself.
- recall that the current date in YYYY-MM-DD format is {current_date} 
- when asked for a season, you must query season_name with "English Premier League YYYY/YY Season" format
- when asked for data about matches, return the entire match column. 
- full_time_result is either "H" (home win), "A" (away win), or "D" (draw)
- half_time_result is either "H" (home win), "A" (away win), or "D" (draw)

The schema is: 
CREATE TABLE public.referee (
	id serial4 NOT NULL,
	"name" varchar NOT NULL,
	CONSTRAINT referee_pkey PRIMARY KEY (id)
);
CREATE UNIQUE INDEX ix_referee_name ON public.referee USING btree (name);

CREATE TABLE public.season (
	id serial4 NOT NULL,
	"name" varchar NOT NULL,
	CONSTRAINT season_pkey PRIMARY KEY (id)
);
CREATE UNIQUE INDEX ix_season_name ON public.season USING btree (name);

CREATE TABLE public.team (
	id serial4 NOT NULL,
	"name" varchar NOT NULL,
	CONSTRAINT team_pkey PRIMARY KEY (id)
);
CREATE UNIQUE INDEX ix_team_name ON public.team USING btree (name);


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
	asian_handicap_line float8 NULL,
	bet365_asian_handicap_home_odds float8 NULL,
	bet365_asian_handicap_away_odds float8 NULL,
	pinnacle_asian_handicap_home_odds float8 NULL,
	pinnacle_asian_handicap_away_odds float8 NULL,
	max_asian_handicap_home_odds float8 NULL,
	max_asian_handicap_away_odds float8 NULL,
	avg_asian_handicap_home_odds float8 NULL,
	avg_asian_handicap_away_odds float8 NULL,
	CONSTRAINT match_pkey PRIMARY KEY (id),
	CONSTRAINT match_away_team_name_fkey FOREIGN KEY (away_team_name) REFERENCES public.team("name"),
	CONSTRAINT match_home_team_name_fkey FOREIGN KEY (home_team_name) REFERENCES public.team("name"),
	CONSTRAINT match_referee_name_fkey FOREIGN KEY (referee_name) REFERENCES public.referee("name"),
	CONSTRAINT match_season_name_fkey FOREIGN KEY (season_name) REFERENCES public.season("name")
);

CREATE TABLE public.stadium (
	id serial4 NOT NULL,
	"name" varchar NOT NULL,
	home_team varchar NULL,
	CONSTRAINT stadium_pkey PRIMARY KEY (id),
	CONSTRAINT stadium_home_team_fkey FOREIGN KEY (home_team) REFERENCES public.team("name")
);
CREATE INDEX ix_stadium_name ON public.stadium USING btree (name);


CREATE TABLE public.teamseason (
	id serial4 NOT NULL,
	team_name varchar NULL,
	season_name varchar NULL,
	CONSTRAINT teamseason_pkey PRIMARY KEY (id),
	CONSTRAINT teamseason_season_name_fkey FOREIGN KEY (season_name) REFERENCES public.season("name"),
	CONSTRAINT teamseason_team_name_fkey FOREIGN KEY (team_name) REFERENCES public.team("name")
);

```sql
"""


ANSWER_BOT_SYSTEM_PROMPT = """
You are a question answer bot. The user will provide some dictionaries with match data and their original question. 
You task is to frame an answer that is relevant to the question and the data provided.
"""

ANSWER_BOT_USER_PROMPT = """
This is the original question {user_question}
And this is the query result as a list dictionaries {match_data}.

Frame an answer to the question and return the response in Markdown with only bold, italics, lists and quotes. Do not use headers. 
"""


class StatsRequest(BaseModel):
    message: str


client = Together(api_key=os.environ.get("TOGETHER_API_KEY"))


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
        model="meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
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
            model="meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
        )

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"There currently is a problem with the service. Please try again.",
        )

    response = chat_completions.choices[0].message.content
    return response


excluded_odds = {
    "interwetten_home_win_odds",
    "interwetten_draw_odds",
    "interwetten_away_win_odds",
    "pinnacle_home_win_odds",
    "pinnacle_draw_odds",
    "pinnacle_away_win_odds",
    "william_hill_home_win_odds",
    "william_hill_draw_odds",
    "william_hill_away_win_odds",
    "asian_handicap_home_win_odds",
    "asian_handicap_draw_odds",
    "asian_handicap_away_win_odds",
    "bet365_over_2_5_odds",
    "bet365_under_2_5_odds",
    "pinnacle_over_2_5_odds",
    "pinnacle_under_2_5_odds",
    "max_over_2_5_odds",
    "max_under_2_5_odds",
    "avg_over_2_5_odds",
    "avg_under_2_5_odds",
}


def convert_rows_to_essentials(results: List[Row]) -> dict:
    dicts = [row._asdict() for row in results]

    # Remove None values and odds information
    for d in dicts:
        if "id" in d:
            del d["id"]
        for k, v in list(d.items()):
            if k in excluded_odds:
                del d[k]

    # Check if 'season_name' exists in any of the dictionaries and sort based on it
    if any("match_date" in d for d in dicts):
        sorted_dicts = sorted(dicts, key=lambda x: x.get("match_date", ""), reverse=True)
    else:
        sorted_dicts = dicts  # Keep original order if 'season_name' is not present
    return sorted_dicts
