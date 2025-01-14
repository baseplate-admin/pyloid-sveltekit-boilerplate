import os
from pyloid import Pyloid, get_production_path, is_production
from .bridge import JSApi
from .server import make_app
from .functions import find_free_port
from multiprocessing import Process
from threading import Thread

PORT = find_free_port()

app = Pyloid(app_name="Pyloid-App", single_instance=True)

if is_production():
    production_path = get_production_path()
else:
    production_path = os.getcwd()


if is_production() and production_path:
    app.set_icon(os.path.join(production_path, "icons/icon.png"))
    app.set_tray_icon(os.path.join(production_path, "icons/icon.png"))
else:
    app.set_icon("src-pyloid/icons/icon.png")
    app.set_tray_icon("src-pyloid/icons/icon.png")

server = Thread(
    target=make_app,
    args=(PORT, os.path.join(production_path, "dist-front")),
)
server.daemon = True
server.start()

if is_production() and production_path:
    # production
    window = app.create_window(
        title="Pyloid Browser-production",
        js_apis=[JSApi()],
        dev_tools=False,
    )
    window.load_url(f"http://localhost:{PORT}")
else:
    window = app.create_window(
        title="Pyloid Browser-dev",
        js_apis=[JSApi()],
        dev_tools=True,
    )
    window.load_url("http://localhost:5173")
