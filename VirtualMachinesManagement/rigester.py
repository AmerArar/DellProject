import json
from flask import Flask
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS,cross_origin
import random
from LogeIn import *
app = Flask(__name__)
api = Api(app)

class R_userDTO:

    def __init__(self,ID,username,userpassword):
        self.ID=ID
        self.username=str(username)
        self.userpassword=str(userpassword)

class registration(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name")
        parser.add_argument("password")
        params = parser.parse_args()
        obj=R_userDTO(None,params["name"],params["password"])
        if((obj.username==None)or(obj.userpassword==None)):
            print(" missing arguments")
            return str(False),400

        else:
            res = CreatNewUser(obj.username, obj.userpassword)
            return str(res), 201


api.add_resource(registration, "/registration", "/registration/", "/registration/<string:name>")
if __name__ == '__main__':
    app.run(debug=True)