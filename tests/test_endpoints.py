import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine, SQLModel
from sqlmodel.pool import StaticPool
from datetime import datetime, timedelta

from main import app
from app.database import get_session


@pytest.fixture(name="session")
def session_fixture():
    """Crear una BD SQLite en memoria para los tests."""
    engine = create_engine(
        "sqlite://", 
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    """Crear un cliente de prueba con la BD en memoria."""
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


class TestAutos:
    """Tests para endpoints de Autos."""

    def test_create_auto(self, client: TestClient):
        """Test: Crear un auto."""
        response = client.post(
            "/autos/",
            json={"marca": "Toyota", "modelo": "Corolla", "año": 2023},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["marca"] == "Toyota"
        assert data["modelo"] == "Corolla"
        assert data["año"] == 2023
        assert data["numero_chasis"]  # Debe generarse automáticamente
        assert len(data["numero_chasis"]) == 17

    def test_create_auto_invalid_year(self, client: TestClient):
        """Test: Crear auto con año inválido."""
        response = client.post(
            "/autos/",
            json={"marca": "Ford", "modelo": "Focus", "año": 1800},
        )
        assert response.status_code == 422

    def test_list_autos(self, client: TestClient):
        """Test: Listar autos con paginación."""
        # Crear 3 autos
        for i in range(3):
            client.post(
                "/autos/",
                json={"marca": f"Marca{i}", "modelo": f"Modelo{i}", "año": 2020 + i},
            )
        
        # Listar sin filtros
        response = client.get("/autos/")
        assert response.status_code == 200
        assert len(response.json()) == 3

    def test_list_autos_with_pagination(self, client: TestClient):
        """Test: Listar autos con skip y limit."""
        for i in range(5):
            client.post(
                "/autos/",
                json={"marca": f"Marca{i}", "modelo": f"Modelo{i}", "año": 2020},
            )
        
        response = client.get("/autos/?skip=0&limit=2")
        assert response.status_code == 200
        assert len(response.json()) == 2

    def test_get_auto_by_id(self, client: TestClient):
        """Test: Obtener un auto por ID."""
        create_response = client.post(
            "/autos/",
            json={"marca": "Honda", "modelo": "Civic", "año": 2022},
        )
        auto_id = create_response.json()["id"]
        
        response = client.get(f"/autos/{auto_id}")
        assert response.status_code == 200
        assert response.json()["marca"] == "Honda"

    def test_get_auto_not_found(self, client: TestClient):
        """Test: Obtener auto inexistente."""
        response = client.get("/autos/999")
        assert response.status_code == 404

    def test_delete_auto(self, client: TestClient):
        """Test: Eliminar un auto."""
        create_response = client.post(
            "/autos/",
            json={"marca": "Chevrolet", "modelo": "Cruze", "año": 2021},
        )
        auto_id = create_response.json()["id"]
        
        delete_response = client.delete(f"/autos/{auto_id}")
        assert delete_response.status_code == 204
        
        # Verificar que fue eliminado
        get_response = client.get(f"/autos/{auto_id}")
        assert get_response.status_code == 404


class TestVentas:
    """Tests para endpoints de Ventas."""

    def test_create_venta(self, client: TestClient):
        """Test: Crear una venta."""
        # Crear un auto primero
        auto_response = client.post(
            "/autos/",
            json={"marca": "Toyota", "modelo": "Corolla", "año": 2023},
        )
        auto_id = auto_response.json()["id"]
        
        # Crear una venta
        venta_data = {
            "nombre_comprador": "Juan Pérez",
            "precio": 25000.00,
            "fecha_venta": (datetime.now() - timedelta(days=1)).isoformat(),
            "auto_id": auto_id,
        }
        response = client.post("/ventas/", json=venta_data)
        assert response.status_code == 201
        data = response.json()
        assert data["nombre_comprador"] == "Juan Pérez"
        assert data["precio"] == 25000.00

    def test_create_venta_auto_not_found(self, client: TestClient):
        """Test: Crear venta con auto inexistente."""
        venta_data = {
            "nombre_comprador": "María García",
            "precio": 30000.00,
            "fecha_venta": (datetime.now() - timedelta(days=1)).isoformat(),
            "auto_id": 999,
        }
        response = client.post("/ventas/", json=venta_data)
        assert response.status_code == 404

    def test_create_venta_invalid_price(self, client: TestClient):
        """Test: Crear venta con precio inválido."""
        auto_response = client.post(
            "/autos/",
            json={"marca": "Ford", "modelo": "Focus", "año": 2022},
        )
        auto_id = auto_response.json()["id"]
        
        venta_data = {
            "nombre_comprador": "Carlos López",
            "precio": -5000.00,  # Precio negativo inválido
            "fecha_venta": (datetime.now() - timedelta(days=1)).isoformat(),
            "auto_id": auto_id,
        }
        response = client.post("/ventas/", json=venta_data)
        assert response.status_code == 422

    def test_create_venta_future_date(self, client: TestClient):
        """Test: Crear venta con fecha en el futuro."""
        auto_response = client.post(
            "/autos/",
            json={"marca": "Honda", "modelo": "Civic", "año": 2023},
        )
        auto_id = auto_response.json()["id"]
        
        venta_data = {
            "nombre_comprador": "Ana Martínez",
            "precio": 28000.00,
            "fecha_venta": (datetime.now() + timedelta(days=1)).isoformat(),  # Futuro
            "auto_id": auto_id,
        }
        response = client.post("/ventas/", json=venta_data)
        assert response.status_code == 422

    def test_list_ventas(self, client: TestClient):
        """Test: Listar ventas."""
        # Crear auto
        auto_response = client.post(
            "/autos/",
            json={"marca": "Chevrolet", "modelo": "Cruze", "año": 2020},
        )
        auto_id = auto_response.json()["id"]
        
        # Crear 2 ventas
        for i in range(2):
            venta_data = {
                "nombre_comprador": f"Comprador{i}",
                "precio": 20000.00 + i * 1000,
                "fecha_venta": (datetime.now() - timedelta(days=1)).isoformat(),
                "auto_id": auto_id,
            }
            client.post("/ventas/", json=venta_data)
        
        response = client.get("/ventas/")
        assert response.status_code == 200
        assert len(response.json()) >= 2

    def test_get_ventas_by_comprador(self, client: TestClient):
        """Test: Buscar ventas por nombre de comprador."""
        # Crear auto
        auto_response = client.post(
            "/autos/",
            json={"marca": "BMW", "modelo": "X5", "año": 2023},
        )
        auto_id = auto_response.json()["id"]
        
        # Crear venta
        venta_data = {
            "nombre_comprador": "Roberto Fernández",
            "precio": 50000.00,
            "fecha_venta": (datetime.now() - timedelta(days=1)).isoformat(),
            "auto_id": auto_id,
        }
        client.post("/ventas/", json=venta_data)
        
        # Buscar por comprador
        response = client.get("/ventas/comprador/Roberto")
        assert response.status_code == 200
        assert len(response.json()) >= 1

    def test_delete_venta(self, client: TestClient):
        """Test: Eliminar una venta."""
        # Crear auto
        auto_response = client.post(
            "/autos/",
            json={"marca": "Audi", "modelo": "A4", "año": 2021},
        )
        auto_id = auto_response.json()["id"]
        
        # Crear venta
        venta_data = {
            "nombre_comprador": "Sofía González",
            "precio": 35000.00,
            "fecha_venta": (datetime.now() - timedelta(days=1)).isoformat(),
            "auto_id": auto_id,
        }
        venta_response = client.post("/ventas/", json=venta_data)
        venta_id = venta_response.json()["id"]
        
        # Eliminar
        delete_response = client.delete(f"/ventas/{venta_id}")
        assert delete_response.status_code == 204
        
        # Verificar que fue eliminada
        get_response = client.get(f"/ventas/{venta_id}")
        assert get_response.status_code == 404
