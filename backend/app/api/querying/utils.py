import requests
from app.core.config import settings
from pydantic import BaseModel

# The following prompt has 2 variables:
# - user_question: str
# - current_date: str

PROMPT = """
<|begin_of_text|><|start_header_id|>user<|end_header_id|>
Generate a SQL query to answer this question: `{user_question}`
- if the question cannot be answered given the database schema, return "I do not know"
- recall that the current date in YYYY-MM-DD format is {current_date} 
- full_time_result is either "H" (home win), "A" (away win), or "D" (draw)
- half_time_result is either "H" (home win), "A" (away win), or "D" (draw)

DDL statements:
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
);|eot_id|><|start_header_id|>assistant<|end_header_id|>

Only answer with the best SQL query to answer the question `{user_question}`:
```sql
"""


headers = {
    "Accept": "application/json",
    "Authorization": f"Bearer {settings.NL2SQL_API_KEY}",
    "Content-Type": "application/json",
}


def query(payload):
    response = requests.post(settings.NL2SQL_API_URL, headers=headers, json=payload)
    return response.json()


class StatsRequest(BaseModel):
    message: str
