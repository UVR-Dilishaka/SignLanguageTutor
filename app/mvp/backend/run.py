from main import create_app
from config import Devconfig


app = create_app(Devconfig)

if __name__ == '__main__':
    app.run(debug=True)