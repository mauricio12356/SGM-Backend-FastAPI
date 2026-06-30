from fastapi.testclient import TestClient

from app.main import app


def auth_headers(client: TestClient) -> dict[str, str]:
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "admin@test.local", "password": "Admin123*"},
    )
    assert response.status_code == 200, response.text
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


def test_health() -> None:
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"


def test_catalog_sale_and_reports() -> None:
    with TestClient(app) as client:
        headers = auth_headers(client)
        category = client.post(
            "/api/v1/categories",
            headers=headers,
            json={"name": "Bebidas", "description": "Bebidas"},
        )
        assert category.status_code == 201, category.text
        product = client.post(
            "/api/v1/products",
            headers=headers,
            json={
                "barcode": "786000000100",
                "name": "Agua",
                "description": "500 ml",
                "purchase_price": "0.25",
                "sale_price": "0.50",
                "current_stock": 10,
                "minimum_stock": 2,
                "category_id": category.json()["id"],
            },
        )
        assert product.status_code == 201, product.text
        sale = client.post(
            "/api/v1/sales",
            headers=headers,
            json={
                "payment_method": "CASH",
                "customer_name": "Consumidor final",
                "customer_tax_id": "9999999999999",
                "details": [{"product_id": product.json()["id"], "quantity": 2}],
            },
        )
        assert sale.status_code == 201, sale.text
        assert sale.json()["total"] == "1.15"
        summary = client.get("/api/v1/reports/sales-summary", headers=headers)
        assert summary.status_code == 200
        assert summary.json()["sales_count"] == 1
