from app.api.querying import stats
from app.api.routes import match, referee, season, team
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(season.router, prefix="/season", tags=["seasons"])
api_router.include_router(team.router, prefix="/team", tags=["teams"])
api_router.include_router(match.router, prefix="/match", tags=["matches"])
api_router.include_router(referee.router, prefix="/referee", tags=["referees"])
api_router.include_router(stats.router, prefix="/query", tags=["querying"])
