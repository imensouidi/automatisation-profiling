from api import app as api_app
from app import app as web_app
import threading

api_thread = threading.Thread(target=api_app.run)
api_thread.start()


web_app.run()
