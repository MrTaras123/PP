from flask import Flask
from wsgiref.simple_server import make_server
app = Flask(__name__)


@app.route('/')
def main_page():
    return "Hello, World!"


@app.route('/api/v1/hello-world-10')
def option():
    return "Hello, World 10!"


with make_server('', 5000, app) as server:
    print("Serving on port 5000...\nVisit http://127.0.0.1:5000/")
    server.serve_forever()


if __name__ == "__main__":
    app.run(debug=True)