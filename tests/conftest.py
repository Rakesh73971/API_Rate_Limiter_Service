from fastapi.testclient import TestClient
from app.main import app
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base,get_db
from app.oauth2 import create_access_token
import pytest
from app.services.rate_limit_service import rate_limiter


SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(bind=engine,autoflush=False,autocommit=False,expire_on_commit=False)

Base.metadata.create_all(bind=engine)

@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db=TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_rate_limiter():
    return None


@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[rate_limiter] = override_rate_limiter
    yield TestClient(app)

@pytest.fixture
def test_user(client):
    user_data = {
        "full_name": "Rakesh",
        "email": "Rakesh@gmail.com",
        "password": "password123",
        "role": "admin"
    }

    response = client.post('/users/', json=user_data)

    assert response.status_code == 201
    new_user = response.json()
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id":test_user['id']})

@pytest.fixture
def authorized_access(client,token):
    client.headers = {
        **client.headers,
        'Authorization':f'Bearer {token}'
    }
    return client

@pytest.fixture
def create_request_log(authorized_access):
    request_data = {
        "endpoint": "/users",
        "status_code": 200,
        "method": "GET"
    }

    response = authorized_access.post("/request_logs/", json=request_data)
    return response.json()

@pytest.fixture
def create_rate_limit_rule(authorized_access):
    request_data = {
        "role":"admin",
        "requests_limit":50,
        "time_window":60
    }

    response = authorized_access.post('/rate_limit_rules/',json=request_data)
    return response.json()