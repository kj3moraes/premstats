from collections.abc import Generator

import pytest
from app.core.db import engine
from app.main import app
from app.pre_start import init_db
from fastapi.testclient import TestClient
from sqlmodel import Session


@pytest.fixture(scope="session", autouse=True)
def db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        init_db(session)
        yield session


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c
