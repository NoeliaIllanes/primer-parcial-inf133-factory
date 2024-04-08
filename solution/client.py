import requests
import json

def create_order(order_data):
    url = "http://localhost:8000/orders"
    headers = {'Content-type': 'application/json'}
    response = requests.post(url, data=json.dumps(order_data), headers=headers)
    print(response.json())


def get_orders(params=None):
    url = "http://localhost:8000/orders"
    if params:
        url += '?' + '&'.join([f"{key}={value}" for key, value in params.items()])
    response = requests.get(url)
    print(response.json())


def update_order(order_id, update_data):
    url = f"http://localhost:8000/orders/{order_id}"
    headers = {'Content-type': 'application/json'}
    response = requests.put(url, data=json.dumps(update_data), headers=headers)
    print(response.json())


def delete_order(order_id):
    url = f"http://localhost:8000/orders/{order_id}"
    response = requests.delete(url)
    print(response.json())


if __name__ == "__main__":
    # Ejemplos de uso
    create_order({
        "client": "Juan Perez",
        "status": "Pendiente",
        "payment": "Tarjeta de Crédito",
        "shipping": 10.0,
        "products": ["Camiseta", "Pantalón", "Zapatos"],
        "order_type": "Física"
    })

    create_order({
        "client": "Maria Rodriguez",
        "status": "Pendiente",
        "payment": "PayPal",
        "code": "ABC123",
        "expiration": "2022-12-31",
        "order_type": "Digital"
    })

    get_orders()

    update_order(1, {"status": "En Proceso"})

    delete_order(1)

    get_orders()
