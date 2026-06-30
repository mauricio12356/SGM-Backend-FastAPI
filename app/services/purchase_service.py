from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal, ROUND_HALF_UP

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import InventoryMovement, PurchaseOrder, PurchaseOrderDetail, User
from app.repositories import ProductRepository, PurchaseOrderRepository, SupplierRepository
from app.schemas import PurchaseOrderCreate


class PurchaseOrderService:
    def __init__(self) -> None:
        self.orders = PurchaseOrderRepository()
        self.products = ProductRepository()
        self.suppliers = SupplierRepository()

    def create(self, db: Session, payload: PurchaseOrderCreate, administrator: User) -> PurchaseOrder:
        supplier = self.suppliers.get(db, payload.supplier_id)
        if not supplier or not supplier.active:
            raise HTTPException(status_code=404, detail="Proveedor no encontrado")
        order = PurchaseOrder(
            supplier_id=supplier.id,
            administrator_id=administrator.id,
            state="PENDING",
            total=Decimal("0"),
        )
        db.add(order)
        db.flush()
        total = Decimal("0")
        seen: set[int] = set()
        for line in payload.details:
            if line.product_id in seen:
                raise HTTPException(status_code=422, detail="No repita productos en la orden")
            seen.add(line.product_id)
            product = self.products.get(db, line.product_id)
            if not product:
                raise HTTPException(status_code=404, detail=f"Producto {line.product_id} no encontrado")
            subtotal = (line.agreed_price * line.quantity).quantize(Decimal("0.01"), ROUND_HALF_UP)
            total += subtotal
            order.details.append(
                PurchaseOrderDetail(
                    product_id=product.id,
                    quantity=line.quantity,
                    agreed_price=line.agreed_price,
                    subtotal=subtotal,
                )
            )
        order.total = total.quantize(Decimal("0.01"), ROUND_HALF_UP)
        db.commit()
        return self.orders.get(db, order.id)  # type: ignore[return-value]

    def receive(self, db: Session, order_id: int, administrator: User) -> PurchaseOrder:
        order = self.orders.get(db, order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Orden no encontrada")
        if order.state != "PENDING":
            raise HTTPException(status_code=409, detail="Solo se reciben órdenes pendientes")
        for detail in order.details:
            product = self.products.get(db, detail.product_id)
            if product:
                previous = product.current_stock
                product.current_stock += detail.quantity
                product.purchase_price = detail.agreed_price
                db.add(
                    InventoryMovement(
                        movement_type="IN",
                        quantity=detail.quantity,
                        reference=f"PURCHASE-{order.id}",
                        previous_stock=previous,
                        new_stock=product.current_stock,
                        product_id=product.id,
                        user_id=administrator.id,
                    )
                )
        order.state = "RECEIVED"
        order.delivery_date = datetime.now(UTC)
        db.commit()
        return self.orders.get(db, order.id)  # type: ignore[return-value]
