from fastapi import APIRouter
from app.api.routes import season, team, match, referee

api_router = APIRouter()
api_router.include_router(season.router, prefix="/season", tags=["seasons"])
api_router.include_router(team.router, prefix="/team", tags=["teams"])
api_router.include_router(match.router, prefix="/match", tags=["matches"])
api_router.include_router(referee.router, prefix="/referee", tags=["referees"])
