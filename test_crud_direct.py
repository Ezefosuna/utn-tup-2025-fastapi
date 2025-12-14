#!/usr/bin/env python3
"""
Script para testear el CRUD de Autos y Ventas directamente en la base de datos
using SQLModel, Models y Repository (sin FastAPI)

Uso: python test_crud_direct.py
"""

from database import get_session
from models import Auto, AutoCreate, AutoUpdate, Venta, VentaCreate, VentaUpdate
from repository import AutoRepository, VentaRepository
from sqlmodel import create_engine, SQLModel, Session
import sys

# Use an in-memory SQLite database for testing
engine = create_engine("sqlite:///:memory:", echo=False)

def print_header(title: str):
    """Imprime un header con estilo"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def run_automated_tests():
    """Corre tests automatizados para Autos y Ventas"""
    print_header("INICIANDO TESTS AUTOMATIZADOS")
    
    # Crear tablas en la base de datos en memoria
    SQLModel.metadata.create_all(engine)
    
    with Session(engine) as session:
        auto_repo = AutoRepository(session)
        venta_repo = VentaRepository(session)
        
        # === TESTS PARA AUTOS ===
        print("\n--- INICIANDO TESTS DE AUTOS ---")
        
        # 1. Crear Auto
        print("Test 1: Creando un auto...")
        auto_create = AutoCreate(marca="Toyota", modelo="Corolla", año=2022, numero_chasis="CHASIS123")
        nuevo_auto = auto_repo.create(auto_create)
        assert nuevo_auto.id is not None
        assert nuevo_auto.marca == "Toyota"
        print("✅ Test 1: PASSED")

        # 2. Obtener Auto por ID
        print("\nTest 2: Obteniendo auto por ID...")
        auto_obtenido = auto_repo.get_by_id(nuevo_auto.id)
        assert auto_obtenido is not None
        assert auto_obtenido.id == nuevo_auto.id
        print("✅ Test 2: PASSED")

        # 3. Listar Autos
        print("\nTest 3: Listando autos...")
        auto_create_2 = AutoCreate(marca="Honda", modelo="Civic", año=2023, numero_chasis="CHASIS456")
        auto_repo.create(auto_create_2)
        autos = auto_repo.get_all()
        assert len(autos) == 2
        assert autos[0].marca == "Toyota"
        assert autos[1].marca == "Honda"
        print("✅ Test 3: PASSED")

        # 4. Actualizar Auto
        print("\nTest 4: Actualizando un auto...")
        auto_update = AutoUpdate(modelo="Corolla Cross")
        auto_actualizado = auto_repo.update(nuevo_auto.id, auto_update)
        assert auto_actualizado.modelo == "Corolla Cross"
        print("✅ Test 4: PASSED")

        # 5. Eliminar Auto
        print("\nTest 5: Eliminando un auto...")
        exito = auto_repo.delete(nuevo_auto.id)
        assert exito is True
        auto_eliminado = auto_repo.get_by_id(nuevo_auto.id)
        assert auto_eliminado is None
        print("✅ Test 5: PASSED")

        print("\n--- TESTS DE AUTOS FINALIZADOS ---")

        # === TESTS PARA VENTAS ===
        print("\n--- INICIANDO TESTS DE VENTAS ---")

        # Preparar un auto para las ventas
        auto_para_venta = auto_repo.get_all()[0] # Debería ser el Honda Civic

        # 1. Crear Venta
        print("\nTest 1: Creando una venta...")
        venta_create = VentaCreate(
            auto_id=auto_para_venta.id,
            monto=25000.0,
            comprador_nombre="Juan Perez"
        )
        nueva_venta = venta_repo.create(venta_create)
        assert nueva_venta.id is not None
        assert nueva_venta.comprador_nombre == "Juan Perez"
        assert nueva_venta.auto_id == auto_para_venta.id
        print("✅ Test 1: PASSED")

        # 2. Obtener Venta por ID
        print("\nTest 2: Obteniendo venta por ID...")
        venta_obtenida = venta_repo.get_by_id(nueva_venta.id)
        assert venta_obtenida is not None
        assert venta_obtenida.id == nueva_venta.id
        print("✅ Test 2: PASSED")

        # 3. Listar Ventas
        print("\nTest 3: Listando ventas...")
        ventas = venta_repo.get_all()
        assert len(ventas) == 1
        print("✅ Test 3: PASSED")

        # 4. Actualizar Venta
        print("\nTest 4: Actualizando una venta...")
        venta_update = VentaUpdate(monto=26000.0)
        venta_actualizada = venta_repo.update(nueva_venta.id, venta_update)
        assert venta_actualizada.monto == 26000.0
        print("✅ Test 4: PASSED")
        
        # 5. Eliminar Venta
        print("\nTest 5: Eliminando una venta...")
        exito_venta = venta_repo.delete(nueva_venta.id)
        assert exito_venta is True
        venta_eliminada = venta_repo.get_by_id(nueva_venta.id)
        assert venta_eliminada is None
        print("✅ Test 5: PASSED")
        
        print("\n--- TESTS DE VENTAS FINALIZADOS ---")

    print_header("TODOS LOS TESTS PASARON EXITOSAMENTE")

def main():
    """Función principal"""
    try:
        run_automated_tests()
    except Exception as e:
        print(f"\n❌ Error durante la ejecución de los tests: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()