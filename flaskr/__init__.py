from flask import Flask

from flaskr import web, auth

from flask_caching import Cache

from werkzeug.routing import BaseConverter

import os

class BooleanConverter(BaseConverter):
    def to_python(self, value):
        return value.lower() in ['true', '1', 'yes']

    def to_url(self, value):
        return str(value).lower()

def create_app():

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    app.url_map.converters['boolean'] = BooleanConverter

    cache = Cache(app, config={'CACHE_TYPE': 'simple'})

    web.bp.cache = cache

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.register_blueprint(web.bp)
    app.register_blueprint(auth.bp)

    from . import db
    db.init_app(app=app)

    return app

if __name__ == "__main__":
    create_app()