import datetime
import pyVmomi;
import pyVim;
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi.SoapAdapter import CONNECTION_POOL_IDLE_TIMEOUT_SEC
import ssl
from vmwc import VMWareClient
import VMDBExpress01
import ConnectTOserver
import VM_Delete
import viewVM
from VM_Delete import delete_vm_by_name
from management import Management


def Main():
    print("begin")
    num=0
    #Connect TO server:
    ConnectTOserver.ConnectTOserver()
    while (num < 5):
        print("---------------------------------------------------")
        print("-- To create a virtual machine press 1           --")
        print("-- To view all virtual machines By User press 2  --")
        print("-- To delete a virtual machine 3                 --")
        print("-- To view available resources, press 4          --")
        print("-- To Exit , Press another key                   --")
        print("---------------------------------------------------")
        num = int(input())

        # CreateVM:
        if num == 1:
            C=Management("vm457", "10.0.0.1", "XP", "on",'1024', '15','30')
            C.CreateVM()

        else:
            # view all VM By User:
            if num == 2:
                viewVM.view_vm_by_name("192.168.174.139", "root", "amer1234")

            else:
                # Delet vm_by name:
                if num == 3:
                    Name = input("Type a virtual machine name to delete : ")
                    VM_Delete.delete_vm_by_name("192.168.174.139", "root", "amer1234", Name)

                else:
                    #view available resources:
                    if num == 4:
                        print("Resources TO DO!!")

                    else:
                        # Exit:
                        break



    print("end")

Main()


