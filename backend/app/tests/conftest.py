from collections.abc import Generator

import pytest
from app.core.db import engine
from app.main import app
from app.models import Team
from fastapi.testclient import TestClient
from sqlmodel import Session, delete


@pytest.fixture(scope="session", autouse=True)
def db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
        statement = delete(Team)
        session.exec(statement)
        session.commit()


@pytest.fixture(scope="module", autouse=True)
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c
