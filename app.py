from flask import Flask
from wsgiref.simple_server import make_server
app = Flask(__name__)


@app.route('/')
def main_page():
    return "Hello, World ! It`s me Mario)"


@app.route('/api/v1/hello-world-10')
def option():
    return "Hello, World !it`s option №10"


with make_server('', 5000, app) as server:
    print("Serving on port 5000...\nVisit http://127.0.0.1:5000/")
    print("second page : http://127.0.0.1:5000/api/v1/hello-world-10 ")
    server.serve_forever()


if __name__ == "__main__":
    app.run(debug=True)