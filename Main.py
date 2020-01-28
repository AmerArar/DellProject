import datetime
import pyVmomi;
import pyVim;
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi.SoapAdapter import CONNECTION_POOL_IDLE_TIMEOUT_SEC
import ssl
from vmwc import VMWareClient
#import connection
import VMDBExpress01

######################################---ConnectAndCreate---#############################
def CreateVMtoEsxi(username,host,password,vmname,numcpu,ramMB,disksizeGB):
    with VMWareClient(host, username, password) as client:
        vm = client.new_virtual_machine(vmname, cpus=numcpu, ram_mb=ramMB, disk_size_gb=disksizeGB)
        vm.configure_bios(boot_delay=5000, boot_order=['network', 'disk'])
        vm.power_on()

######################################---Create Class---#############################
ResourcesdictList = []
def GettingResources(VMCPU,VMmemory,VMstorage):
    ResourcesdictList = [{'AllocationVMCPU': VMCPU,
                           'AllocationVMmemory': VMmemory,
                           'AllocationVMstorage': VMstorage}]

CreatedictList = []
class Create:
    def __init__(self,identify,UserPassword,VMname,TemplateName,VMCPU,VMmemory,VMstorage):
        self.identify=identify
        self.UserPassword=UserPassword
        self.VMname=VMname
        self.TemplateName=TemplateName
        self.VMCPU=VMCPU
        self.VMMemory=VMmemory
        self.VMstorage=VMstorage
        self.CreatedictList = [
            {'identify': identify, 'UserPassword': UserPassword, 'VMname': VMname, 'TemplateName': TemplateName,
             'VMCPU': VMCPU, 'VMmemory': VMmemory, 'VMstorage': VMstorage}]


    # "WIN10", 1, "1G", "1T"
    def CheckResources(self):
        #if (CreatedictList[0]['TemplateName']  == 'WIN10' or CreatedictList[0]['TemplateName'] == 'Linux'):
            #if (CreatedictList[0]['VMCPU'] <= ResourcesdictList[0]['AllocationVMCPU']  &  CreatedictList[0]['VMmemory'] <= ResourcesdictList[0]['AllocationVMmemory'] & CreatedictList[0]['VMstorage'] <=  ResourcesdictList[0]['AllocationVMstorage'] ):
                CreateVMtoEsxi("root", "192.168.174.128", "12345678", "user1Linux", 1, 1024, 12)
                return True
        #return False


    def CreateVM(self):
        if self.CheckResources():
            print("A new virtual machine was started")
            self.StorData()
        else:
            print("A virtual machine cannot be created")
            print("Not enough resources")

    def StorData(self):
        #stor data vm to sql
        VMD = VMDBExpress01.VMDB()
        print("The Data is saved in SQL")



    def printCreatedictList(self):
        for val in self.CreatedictList:
            print(val)



def Main():
    print("begin")
    #Getting resources -Resource extraction from a servant - There is a continuation of the function
    GettingResources(1,1024,10)

    C1=Create("1001","0504747155","OPWIN10","WIN10",1,"1G","1T")
    C1.CreateVM()

    print("end")

Main()











