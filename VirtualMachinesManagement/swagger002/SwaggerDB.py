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




def initialize_app(flask_app):
    configure_app(flask_app)

    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)
    api.add_namespace(blog_posts_namespace)
    api.add_namespace(blog_categories_namespace)
    flask_app.register_blueprint(blueprint)

    db.init_app(flask_app)


app = Flask(__name__)                  #  Create a Flask WSGI application
api = Api(app)
ns = api.namespace('blog/categories', description='Operations related to blog categories')


@ns.route('/')
class CategoryCollection(Resource):

    def get(self):
        """Returns list of blog categories."""
        return get_all_categories()

    @api.response(201, 'Category successfully created.')
    def post(self):
        """Creates a new blog category."""
        create_category(request.json)
        return None, 201


@ns.route('/<int:id>')
@api.response(404, 'Category not found.')
class CategoryItem(Resource):

    def get(self, id):
        """Returns details of a category."""
        return get_category(id)

    @api.response(204, 'Category successfully updated.')
    def put(self, id):
        """Updates a blog category."""
        update_category(id, request.json)
        return None, 204

    @api.response(204, 'Category successfully deleted.')
    def delete(self, id):
        """Deletes blog category."""
        delete_category(id)
        return None, 204