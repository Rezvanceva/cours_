import os

from flask import Flask, render_template, blueprints

from bp_api.views import bp_api
from bp_posts.views import bp_posts
from db import db
from exceptions.data_exceptions import DataSourseError
import config_logger

DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

def create_and_config_app(config_path) -> Flask:

    app = Flask(__name__)
    app.config.from_pyfile(config_path)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USER}:{DB_PASSWORD}@db/{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    config_logger.config(app)
    app.register_blueprint(bp_posts)
    app.register_blueprint(bp_api, url_prefix='/api')
    db.init_app(app)

    return app

app = create_and_config_app("config.py")

@app.errorhandler(404)
def page_error_404(error):
    return f"Ошибка данных - {error}", 404

@app.errorhandler(500)
def page_error_500(error):
    return f"На сервере произошла ошибка - {error}", 500

@app.errorhandler(DataSourseError)
def page_error_data_sourse_error(error):
    return f"Ошибка данных - {error}", 500




if __name__ == '__main__':
    app.run(port=8000, debug=True)

