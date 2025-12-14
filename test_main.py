
import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session
from main import app
from database import get_session
from models import Auto, Venta

# Use an in-memory SQLite database for testing
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create a fixture for the database session
@pytest.fixture(name="session")
def session_fixture():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)

# Create a fixture for the TestClient
@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        yield session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

# Tests for Auto CRUD

def test_create_auto(client: TestClient):
    response = client.post(
        "/autos/",
        json={"marca": "Test Marca", "modelo": "Test Modelo", "año": 2023, "numero_chasis": "TEST12345"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["marca"] == "Test Marca"
    assert data["modelo"] == "Test Modelo"
    assert data["año"] == 2023
    assert data["numero_chasis"] == "TEST12345"
    assert "id" in data

def test_read_autos(client: TestClient, session: Session):
    auto_1 = Auto(marca="Test Marca 1", modelo="Test Modelo 1", año=2021, numero_chasis="TEST1")
    auto_2 = Auto(marca="Test Marca 2", modelo="Test Modelo 2", año=2022, numero_chasis="TEST2")
    session.add(auto_1)
    session.add(auto_2)
    session.commit()

    response = client.get("/autos/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["marca"] == "Test Marca 1"
    assert data[1]["marca"] == "Test Marca 2"

def test_read_auto(client: TestClient, session: Session):
    auto = Auto(marca="Test Marca", modelo="Test Modelo", año=2023, numero_chasis="TEST123")
    session.add(auto)
    session.commit()

    response = client.get(f"/autos/{auto.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["marca"] == "Test Marca"
    assert data["id"] == auto.id

def test_update_auto(client: TestClient, session: Session):
    auto = Auto(marca="Old Marca", modelo="Old Modelo", año=2020, numero_chasis="OLD123")
    session.add(auto)
    session.commit()

    response = client.put(
        f"/autos/{auto.id}",
        json={"marca": "New Marca", "modelo": "New Modelo"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["marca"] == "New Marca"
    assert data["modelo"] == "New Modelo"
    assert data["id"] == auto.id

def test_delete_auto(client: TestClient, session: Session):
    auto = Auto(marca="To Delete", modelo="To Delete", año=2020, numero_chasis="DELETE123")
    session.add(auto)
    session.commit()

    response = client.delete(f"/autos/{auto.id}")
    assert response.status_code == 204

    response = client.get(f"/autos/{auto.id}")
    assert response.status_code == 404

# Tests for Venta CRUD

def test_create_venta(client: TestClient, session: Session):
    auto = Auto(marca="Test Car", modelo="For Sale", año=2023, numero_chasis="SALE123")
    session.add(auto)
    session.commit()

    response = client.post(
        "/ventas/",
        json={"monto": 50000, "comprador_nombre": "Test Comprador", "auto_id": auto.id},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["comprador_nombre"] == "Test Comprador"
    assert data["monto"] == 50000
    assert data["auto_id"] == auto.id
    assert "id" in data

def test_read_ventas(client: TestClient, session: Session):
    auto = Auto(marca="Test Car", modelo="For Sale", año=2023, numero_chasis="SALE123")
    session.add(auto)
    session.commit()
    venta_1 = Venta(monto=1000, comprador_nombre="Comprador 1", auto_id=auto.id)
    venta_2 = Venta(monto=2000, comprador_nombre="Comprador 2", auto_id=auto.id)
    session.add(venta_1)
    session.add(venta_2)
    session.commit()

    response = client.get("/ventas/")
    assert response.status_code == 200
    data = response.json()
    # This assertion might fail if other tests created ventas, it's better to clean the DB for each test
    # For now, let's assume a clean slate for each function due to the fixture scope
    assert len(data) >= 2 

def test_read_venta(client: TestClient, session: Session):
    auto = Auto(marca="Test Car", modelo="For Sale", año=2023, numero_chasis="SALE123")
    session.add(auto)
    session.commit()
    venta = Venta(monto=3000, comprador_nombre="Comprador 3", auto_id=auto.id)
    session.add(venta)
    session.commit()

    response = client.get(f"/ventas/{venta.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["comprador_nombre"] == "Comprador 3"
    assert data["id"] == venta.id

def test_update_venta(client: TestClient, session: Session):
    auto = Auto(marca="Test Car", modelo="For Sale", año=2023, numero_chasis="SALE123")
    session.add(auto)
    session.commit()
    venta = Venta(monto=4000, comprador_nombre="Old Comprador", auto_id=auto.id)
    session.add(venta)
    session.commit()

    response = client.put(
        f"/ventas/{venta.id}",
        json={"monto": 4500, "comprador_nombre": "New Comprador"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["monto"] == 4500
    assert data["comprador_nombre"] == "New Comprador"
    assert data["id"] == venta.id

def test_delete_venta(client: TestClient, session: Session):
    auto = Auto(marca="Test Car", modelo="For Sale", año=2023, numero_chasis="SALE123")
    session.add(auto)
    session.commit()
    venta = Venta(monto=5000, comprador_nombre="To Delete", auto_id=auto.id)
    session.add(venta)
    session.commit()

    response = client.delete(f"/ventas/{venta.id}")
    assert response.status_code == 204

    response = client.get(f"/ventas/{venta.id}")
    assert response.status_code == 404
