import os
from flask import Flask, jsonify
from src.utils.env import get_env_params

from src.exception import InvalidApiException

def create_app():
    # import routes here and add them here

    app = Flask(__name__, instance_relative_config=True)
    env = get_env_params()
    app.config.from_mapping(**env)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.errorhandler(InvalidApiException)
    def invalid_api_usage(e):
        return jsonify(e.to_dict()), e.status_code

    return app
