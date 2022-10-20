from flask import Flask, render_template, blueprints

from bp_api.views import bp_api
from bp_posts.views import bp_posts
from exceptions.data_exceptions import DataSourseError
import config_logger


def create_and_config_app(config_path):

    app = Flask(__name__)

    app.register_blueprint(bp_posts)
    app.register_blueprint(bp_api, url_prefix='/api')

    app.config.from_pyfile(config_path)
    config_logger.config(app)

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

