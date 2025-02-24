from api import app
from authentification.authQueney import create_super_admin  # Import de la fonction
import threading

def run_api():
    app.run(debug=False, host='0.0.0.0', port=5001, use_reloader=False)

if __name__ == '__main__':
    create_super_admin()  # Création automatique du super admin si inexistant

    api_thread = threading.Thread(target=run_api, daemon=True)
    api_thread.start()
    api_thread.join()  # Attendre la fin du thread
