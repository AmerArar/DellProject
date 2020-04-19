from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from requests import put, get
from flask import jsonify
import Esxi




app = Flask(__name__)
api = Api(app)



#viewVMs
GetAllVMS = Esxi.viewAllVM("192.168.174.139", "root", "Amer2020@")
VirtualMachines={'VMS1':GetAllVMS}


##########################
def abort_if_ViewVM_doesnt_exist(ViewVM_id):
    if ViewVM_id not in VirtualMachines:
        abort(404, message="VM {} doesn't exist".format(ViewVM_id))

parser = reqparse.RequestParser()

parser.add_argument('vmname')
parser.add_argument('cpus')
parser.add_argument('ramMB')
parser.add_argument('disksizeGB')
parser.add_argument('OS')


# shows a single VM item
class VM(Resource):
    def get(self, ViewVM_id):
        abort_if_ViewVM_doesnt_exist(ViewVM_id)
        return VirtualMachines[ViewVM_id]



# shows a list of all ViewVM, and lets you POST to add new VMSs
class VMS(Resource):
    def get(self):
        return VirtualMachines

    def post(self):
        args = parser.parse_args()
        ViewVM_id = int(max(VirtualMachines.keys()).lstrip('VMS')) + 1
        ViewVM_id = 'VMS%i' % ViewVM_id

        VirtualMachines[ViewVM_id] = { 'vmname': args['vmname'], 'OS': args['OS'], 'cpus': args['cpus'],
                                      'ramMB': args['ramMB'],'disksizeGB': args['disksizeGB']}
        Esxi.CreateVMtoEsxi('root', '192.168.174.139', 'Amer', args['vmname'], int(args['cpus']),
                       int(args['ramMB']) , int(args['disksizeGB']))

        return VirtualMachines[ViewVM_id], 201

###
def abort_if_DeletVM_doesnt_exist(DeletVM_id):
    if DeletVM_id not in VirtualMachines:
        abort(404, message="VMS {} doesn't exist".format(DeletVM_id))

class DeleteVM(Resource):

    def delete(self, DeletVM_id,vmnames):
        abort_if_DeletVM_doesnt_exist(DeletVM_id)
        print('DeletVM_name:',vmnames)
        Esxi.delete_vm_by_name('192.168.174.139', 'root', 'Amer2020@', vmnames)
        del VirtualMachines[DeletVM_id]
        return '', 204


###


## Actually setup the Api resource routing here
api.add_resource(VMS, '/VMS')
api.add_resource(VM, '/VMS/<ViewVM_id>')
api.add_resource(DeleteVM, '/VMS/<DeletVM_id>/<vmnames>')

#if __name__ == '__main__':
app.run(debug=True)


#http://127.0.0.1:5000/

# View All VMS:
#http://localhost:5000/VMS

# view_vm_by_name:
#http://localhost:5000/VMS/VMS1

# Creat new VM:
#http://localhost:5000/VMS?vmname=VMlinux&cpus=2&ramMB=1024&disksizeGB=3&OS=linux

# Delete VM:
#http://localhost:5000/VMS/VMS2/VMlinux
