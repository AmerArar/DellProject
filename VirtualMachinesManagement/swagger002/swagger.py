try:
    import flask
    from flask import request, Flask
    from flask_restful import Resource, Api

    from flask_limiter.util import get_remote_address
    from flask_limiter import Limiter

    from flasgger import Swagger
    from flasgger.utils import  swag_from
    from flask_restful_swagger import swagger

except Exception as e:
    print("Some modules are missing {}".format(e))


app = Flask(__name__)
api = Api(app)


limiter = Limiter(app, key_func=get_remote_address)
limiter.init_app(app)

api_swagger = swagger.docs(api, apiVersion='0.1', api_spec_url = '/docs')




class MyVMapi(Resource):

    decorators = [limiter.limit("10/day")]
    @swagger.model
    @swagger.operation(notes="good !!!")

    def get(self, ID):
        return {
            "Resources":200,
            'Data':ID
        }


api.add_resource(MyVMapi,'/VM/<string:ID>')
if __name__=="__main__":
    app.run(debug=True)







# http://127.0.0.1:5000/docs