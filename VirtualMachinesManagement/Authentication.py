import json
from flask import Flask
from flask_restful import Api, Resource, reqparse
import random
from  DataBase import  LogIn
from LogIn import *


app = Flask(__name__)
api = Api(app)


class userDTO:

    def __init__(self,ID,username,userpassword):
        self.ID=ID
        self.username=str(username)
        self.userpassword=str(userpassword)

class authentication(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name")
        parser.add_argument("password")
        params = parser.parse_args()
        obj=userDTO(None,params["name"],params["password"])
        if((obj.username==None)or(obj.userpassword==None)):
            print(" missing arguments")
            return str(False),400
        else:
            res = CheckLogIn(obj.username, obj.userpassword)
            return str(res), 200


api.add_resource(authentication, "/auth", "/auth/", "/auth/<string:name>")
if __name__ == '__main__':
    app.run(debug=True)
