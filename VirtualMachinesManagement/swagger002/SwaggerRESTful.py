from sqlalchemy.testing import db

try:
    import flask
    import flask_blueprint
    import flask_sqlalchemy
    from flask import request, Flask, Blueprint
    from flask_restful import Resource, Api

    from flask_limiter.util import get_remote_address
    from flask_limiter import Limiter

    from flasgger import Swagger
    from flasgger.utils import  swag_from
    from flask_restful_swagger import swagger

except Exception as e:
    print("Some modules are missing {}".format(e))

app = Flask(__name__)                  #  Create a Flask WSGI application
api = Api(app)


class HelloWorld(Resource):            #  Create a RESTful resource
    def get(self):                     #  Create GET endpoint
        return {'hello': 'world'}



if __name__ == '__main__':
    app.run(debug=True)
