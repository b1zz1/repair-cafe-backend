from flask import Flask, request
from flask_cors import CORS
from routes.user_routes import user_bp

app = Flask(__name__)
cors = CORS(app, resources={r"/user/*": {"origins": "http://localhost:3000"}})

app.register_blueprint(user_bp)


@app.route('/')
@app.route('/home')
def index():
    return "Hello, World!"


if __name__ == '__main__':
    app.run(debug=True)
