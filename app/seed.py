from decimal import Decimal

from app.core.config import settings
from app.core.database import Base, SessionLocal, engine
from app.models import Category, Product, Supplier
from app.services import AuthService


def seed() -> None:
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        AuthService().ensure_default_admin(db, settings.default_admin_email, settings.default_admin_password)
        if db.query(Category).count() == 0:
            groceries = Category(name="Abarrotes", description="Productos de consumo diario")
            drinks = Category(name="Bebidas", description="Bebidas frías y calientes")
            db.add_all([groceries, drinks])
            db.flush()
            db.add_all(
                [
                    Product(
                        barcode="786000000001",
                        name="Arroz 1 kg",
                        description="Arroz blanco",
                        purchase_price=Decimal("0.90"),
                        sale_price=Decimal("1.20"),
                        current_stock=30,
                        minimum_stock=5,
                        category_id=groceries.id,
                    ),
                    Product(
                        barcode="786000000002",
                        name="Agua 500 ml",
                        description="Agua sin gas",
                        purchase_price=Decimal("0.25"),
                        sale_price=Decimal("0.50"),
                        current_stock=50,
                        minimum_stock=10,
                        category_id=drinks.id,
                    ),
                ]
            )
        if db.query(Supplier).count() == 0:
            db.add(
                Supplier(
                    name="Distribuidora Ejemplo S.A.",
                    tax_id="0999999999001",
                    phone="0999999999",
                    email="ventas@proveedor.local",
                    address="Guayaquil, Ecuador",
                )
            )
        db.commit()
    print("Datos iniciales creados correctamente.")


if __name__ == "__main__":
    seed()
