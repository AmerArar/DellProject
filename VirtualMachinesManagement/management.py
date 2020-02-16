import DB
import ESXI
import pyVmomi
import pyvim
import uuid
import connection


class Management:
    def __init__(self, VMName, Ip, OperatingSystem, Status, Ram, Storage, LifeTime):
        self.VMName = VMName
        self.Ip = Ip
        self.OperatingSystem = OperatingSystem
        self.Status = Status
        self.Ram = Ram
        self.Storage = Storage
        self.LifeTime = LifeTime
    def LogIn(self,UserName,Password):
        #if  user name and password are true in the data base
        #return UniqueiD /and save it in sql
        pass
    def CreateVM_(self):
        # check if the vm name already exist if not then
        # check if the vm data exist in the esxi
        # if true the create vm
        # save on SQL
        pass

    def DeleteVM_(self,VMid,host):
            DB.VMDB().deleteFromVMDB(VMid)  # delete by vm UniqueiD
            print("VM Deleted from SQL")
            res=ESXI.ManageESXI().Delete(VMid,host)#delete by vm  UniqueiD
            if(res==False):
                print("vm Dose not Exist")
            else:
                print("VM Deleted from Esxi 6.5")
    def FindVMID(self,VMName,UniqueiD):
         connection.connections() #connect to data base
         ListOfVMs=[]
         ListOfVMs=DB.GetAllVMsForThisUser(UniqueiD)
       #  for i in ListOfVMs:
             #sent to def (i[2])
         #  DB.VMDB().Search(UniqueiD)#searsh by UniqueiD
          #if exist
          # return ip_address
    def GetAllVMs(self,content):
        ListVMDB = []
        ListVMEsxi={}
        newlist=[]
        ListVMDB=DB.VMDB().fetchAllVMData()
        ListVMEsxi=ESXI.ManageESXI().Get_All_VM(content)
       # print("all the VM's that have been saved on the Data Base SQL : ")
        if (len(ListVMDB) < 1):
            print("this user have no VM's in the Data Base")
        if (ListVMEsxi == None):
            print("there is no vms in the esxi to thes user")
        if (len(ListVMDB) > 1 and ListVMEsxi != None):
            for keys, values in ListVMEsxi.items():
               # print(keys, " : ", values)
                if (keys == 'ip_address'):
                    newlist.append(values)#all the vm ip from the  dictionary that in esxi 6,5 in a new list
            counter=0
            for i in ListVMDB:
                for j in newlist:
                    if(i[3]==j):
                        counter=counter+1
            if (len(ListVMDB)==counter):
                return True
            else:
                return False

          #  for()
    def ExtendVMLifeTime(self,Name, VMIP, OS, LifeTime, Owner, Designation):
         DB.ExtendLifeTime(Name, VMIP, OS, LifeTime, Owner, Designation)
#c=ESXI.ManageESXI().ConnectEsxi()
#dec=ESXI.ManageESXI().Get_All_VM(c)
#m=Management("vm457",12345678,"XP","on",'1','','')#'VMName', 'Ip', 'OperatingSystem', 'Status', 'Ram', 'Storage', and 'LifeTime
#m.DeleteVM_("vm457",'192.168.204.128')
#m.GetAllVMs(c)
#Management.ChekVmInEsxi(dec,"12345678")
MVMList=[]
#M=Management("vm457",12345678, "XP", "on",'1', '', '')
MVMList.append(Management("vm457",12345678, "XP", "on",'1', '', ''))#list of VM's data
