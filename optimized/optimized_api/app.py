import subprocess
from ..lineq import MatrixMethods

def check_flask():
    try:
        import flask
        print("🟢 Flask found.")
    except:
        print("🔴 Flask not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "flask"])
        print("🟢 Flask installed.")
        
def main():
    check_flask()
    from flask import Flask
    from .routes import det, home

    app = Flask(__name__)

# Регистрация маршрутов
    app.add_url_rule('/', 'home', home, methods=['GET'])
    app.add_url_rule('/det/', 'determinant', det, methods=['GET'])

    app.run(debug=True)
    
if __name__ == "__main__":
    main()