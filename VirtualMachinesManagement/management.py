import DB
import ESXI
import pyVmomi
import pyvim
import uuid
import connection
import LogIn

class Management:
    def __init__(self, VMName, Ip, OperatingSystem, Status, Ram, Storage, LifeTime,UniqueiD):
        self.VMName = VMName
        self.Ip = Ip
        self.OperatingSystem = OperatingSystem
        self.Status = Status
        self.Ram = Ram
        self.Storage = Storage
        self.LifeTime = LifeTime
        self.UniqueiD=UniqueiD
    def LogIn(self,UserName,Password):
       LogIn.LogeIn().CheckLogIn(UserName,Password)
    def CreateVM_(self):
        # check if the vm name already exist if not then
        # check if the vm data exist in the esxi
        # if true the create vm
        #create Log in
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
    def GetAllVMsFromSQL(self,PassWord,VMName):#only from SQL
        ListOfUniqueiD=[]
        ListOfAllVMs=[]
        if(LogIn.LogeIn().CheckLogIn('root',PassWord)):
           listUsers = LogIn.LogeIn().AllUsers()
           for i in listUsers:
               ListOfUniqueiD.append(i[2])
        ListOfAllVMs=DB.VMDB().fetchAllVMData()
        for i in ListOfAllVMs:
            for j in ListOfUniqueiD:
               if(i[8]==j and VMName==i[1]):#i[8]==> UniqueiD ,i[1]==> VM name
                   print(i)
                   return i
    def checkGetAllVMs(self):
        c=ESXI.ManageESXI().ConnectEsxi()
        dicVM=ESXI.ManageESXI().Get_All_VM(c)
        ListVMDB = []
        newlist = []
        ListVMDB = DB.VMDB().fetchAllVMData()
        # print("all the VM's that have been saved on the Data Base SQL : ")
        if (len(ListVMDB) < 1):
            print("this user have no VM's in the Data Base")
        if (dicVM == None):
            print("there is no vms in the esxi to thes user")
        if (len(ListVMDB) > 1 and dicVM != None):
            for keys, values in dicVM.items():
                # print(keys, " : ", values)
                if (keys == 'ip_address'):
                    newlist.append(values)  # all the vm ip from the  dictionary that in esxi 6,5 in a new list
            counter = 0
            for i in ListVMDB:
                for j in newlist:
                    if (i[3] == j):
                        counter = counter + 1
            if (len(ListVMDB) == counter):
                return True
            else:
                return False
    def GetAllVMs(self,PassWord,VMName):
        if(self.checkGetAllVMs()):# not shore
            self.GetAllVMsFromSQL(PassWord,VMName)
    def ExtendVMLifeTime(self,PassWord,VMName):
        DB.VMDB().ExtendLifeTime(PassWord,VMName)


#c=ESXI.ManageESXI().ConnectEsxi()
#dec=ESXI.ManageESXI().Get_All_VM(c)
#m=Management("vm457",12345678,"XP","on",'1','','')#'VMName', 'Ip', 'OperatingSystem', 'Status', 'Ram', 'Storage', and 'LifeTime
#m.DeleteVM_("vm457",'192.168.204.128')
#m.GetAllVMs(c)
#Management.ChekVmInEsxi(dec,"12345678")
MVMList=[]
#M=Management("vm457",12345678, "XP", "on",'1', '', '')
MVMList.append(Management("vm457",12345678, "XP", "on",'1', '', ''))#list of VM's data
