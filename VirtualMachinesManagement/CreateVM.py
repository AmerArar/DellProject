import uuid

import pyVmomi;
import pyVim;
from pyVim.connect import SmartConnect, Disconnect
import ssl
import datetime
import connection
from vmwc import VMWareClient
class main_component:
    def connect_(self):
        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        context.verify_mode = ssl.CERT_NONE
        connect = SmartConnect(host="192.168.204.128", user="root", pwd="12345678", port=int("443"), sslContext=context)
        content = connect.RetrieveContent()

    def CreateVM(self,username, host, password, vmname, numcpu, ramMB, disksizeGB):
        with VMWareClient(host, username, password) as client:
           vm = client.new_virtual_machine(vmname, cpus=numcpu, ram_mb=ramMB, disk_size_gb=disksizeGB)
           vm.configure_bios(boot_delay=5000, boot_order=['network', 'disk'])
           vm.uuid=uuid.uuid1()
           vm.power_on()
           create_date = datetime.datetime.now()
           vm_life_time = create_date + datetime.timedelta(days=30)

               # connection = connection().getConnection()
                 # save all that in DB


    def delete_vm(self):
       pass
    def extend_vm_life_time(self):
        pass
def main():
    main_component().connect_()
    main_component().CreateVM()("root","192.168.204.128", "12345678", "v1",2, 1024, 20)


if __name__ == '__main__':
    main()
