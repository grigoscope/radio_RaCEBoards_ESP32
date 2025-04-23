import wifi, socketpool, ipaddress, json
from adafruit_httpserver import Server, Request, Response, Websocket, GET

class WebInterface:
    """HTTP + WebSocket server."""
    def __init__(self, ssid, pwd, html_template, port=5000):
        # Connect to the WiFi network
        wifi.radio.connect(ssid, pwd)
        self.ip   = str(wifi.radio.ipv4_address)  # Store the IP address
        self.port = port  # Store the port number
        pool = socketpool.SocketPool(wifi.radio)  # Create a socket pool
        self.server = Server(pool, debug=True, address_="/client")  # Initialize the HTTP server
        self.html   = html_template  # Store the HTML template
        self.ws     = None  # WebSocket instance
        self._routes()  # Set up routes

    def _routes(self):
        # Define the route to serve the HTML template
        @self.server.route("/client", GET)
        def serve(request: Request):
            return Response(request, self.html, content_type="text/html; charset=utf-8")

        # Define the route to establish a WebSocket connection
        @self.server.route("/connect-websocket", GET)
        def ws_connect(request: Request):
            if self.ws:
                self.ws.close()  # Close the existing WebSocket connection if any
            self.ws = Websocket(request, buffer_size=32768)  # Create a new WebSocket connection
            return self.ws

    def start(self):
        # Start the HTTP server
        self.server.start(self.ip)

    def poll(self):
        # Poll the server for incoming requests
        self.server.poll()

    def send(self, data: dict):
        # Send data through the WebSocket connection if it exists
        if self.ws:
            self.ws.send_message(json.dumps(data), fail_silently=True)
