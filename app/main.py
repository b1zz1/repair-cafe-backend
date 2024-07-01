from flask import Flask
from flask_cors import CORS
from app.user_routes import user_bp
from app.repair_point_routes import repair_point_bp
from database.base import SessionLocal, engine, Base
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

Base.metadata.create_all(bind=engine)

app.register_blueprint(user_bp, url_prefix='/users')
app.register_blueprint(repair_point_bp, url_prefix='/repair_points')

@app.route('/')
@app.route('/home')
def index():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(debug=True)
