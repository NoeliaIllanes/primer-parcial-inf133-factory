from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import json

class OrderFactory:
    @staticmethod
    def create_order(order_type, **kwargs):
        if order_type == "Física":
            return PhysicalOrder(**kwargs)
        elif order_type == "Digital":
            return DigitalOrder(**kwargs)

class Order:
    def __init__(self, client, status, payment, order_type):
        self.client = client
        self.status = status
        self.payment = payment
        self.order_type = order_type


class PhysicalOrder(Order):
    def __init__(self, client, status, payment, shipping, products):
        super().__init__(client, status, payment, "Física")
        self.shipping = shipping
        self.products = products


class DigitalOrder(Order):
    def __init__(self, client, status, payment, code, expiration):
        super().__init__(client, status, payment, "Digital")
        self.code = code
        self.expiration = expiration

class OrderHandler(BaseHTTPRequestHandler):
    orders = {}
    order_counter = 0

    def _set_headers(self, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        post_data = json.loads(post_data.decode('utf-8'))

        order_type = post_data.get("order_type")
        order = OrderFactory.create_order(order_type, **post_data)

        self.order_counter += 1
        self.orders[self.order_counter] = order.__dict__

        self._set_headers()
        self.wfile.write(json.dumps(order.__dict__).encode('utf-8'))

    def do_GET(self):
        url_parsed = urlparse(self.path)
        query_params = parse_qs(url_parsed.query)
        
        if url_parsed.path == '/orders':
            if not query_params:
                self._set_headers()
                self.wfile.write(json.dumps(self.orders).encode('utf-8'))
            elif 'status' in query_params:
                status = query_params['status'][0]
                filtered_orders = {order_id: order for order_id, order in self.orders.items() if order['status'] == status}
                self._set_headers()
                self.wfile.write(json.dumps(filtered_orders).encode('utf-8'))
        else:
            self._set_headers(404)
            self.wfile.write("Ruta no encontrada".encode('utf-8'))

    def do_PUT(self):
        order_id = int(self.path.split('/')[-1])
        content_length = int(self.headers['Content-Length'])
        put_data = self.rfile.read(content_length)
        put_data = json.loads(put_data.decode('utf-8'))

        if order_id in self.orders:
            self.orders[order_id].update(put_data)
            self._set_headers()
            self.wfile.write(json.dumps({str(order_id): self.orders[order_id]}).encode('utf-8'))
        else:
            self._set_headers(404)
            self.wfile.write("Order not found".encode('utf-8'))

    def do_DELETE(self):
        order_id = int(self.path.split('/')[-1])

        if order_id in self.orders:
            del self.orders[order_id]
            self._set_headers()
            self.wfile.write(json.dumps({"message": "Order deleted"}).encode('utf-8'))
        else:
            self._set_headers(404)
            self.wfile.write("Ruta no encontrada".encode('utf-8'))


def run(server_class=HTTPServer, handler_class=OrderHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Iniciando servidor HTTP en puerto {port}...')
    httpd.serve_forever()


if __name__ == "__main__":
    run()
