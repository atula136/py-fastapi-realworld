import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists, drop_database

from alembic import command
from alembic.config import Config

from app.api.deps import get_db
from app.main import app

# Load environment variables
from dotenv import load_dotenv
load_dotenv('.env.test')

TEST_DATABASE_URL = os.getenv("DATABASE_URL")

# Create an engine pointing to your test database
engine = create_engine(TEST_DATABASE_URL)

# Create a session for your test database
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def pytest_configure(config):
    print(f"Running tests with database: {os.getenv('DATABASE_URL')}")

@pytest.fixture(scope="session")
def setup_test_database():
    # Drop the test database if it exists
    if database_exists(engine.url):
        drop_database(engine.url)
        print("Existing test database dropped.")

    # Create a new test database
    create_database(engine.url)
    print(f"Test database created at {engine.url}.")

    # Run migrations
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", TEST_DATABASE_URL)
    command.upgrade(alembic_cfg, "head")
    print("Migrations applied.")

    yield

    # Drop test database after tests are done
    drop_database(engine.url)
    print("\nTest database dropped.")

@pytest.fixture(scope="function")
def db_session(setup_test_database):
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()

def override_get_db(session):
    """Dependency override for the get_db function"""
    def _override_get_db():
        try:
            yield session
        finally:
            session.close()
    return _override_get_db

@pytest.fixture(scope="function")
def test_client(db_session):
    """Create test client with db dependency overridden"""
    app.dependency_overrides[get_db] = override_get_db(db_session)  # Ensure get_db uses the same session
    with TestClient(app) as client:
        yield client
    app.dependency_overrides = {}  # Clean up overrides after test
