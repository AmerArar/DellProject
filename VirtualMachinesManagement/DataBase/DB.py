import pyodbc
import connection
import pandas as pd
import datetime
import uuid
from datetime import timedelta
import LogIn


class VMDB:
    connection = connection.connections().getConnection()

    # cursor = connection.connections().getCursor()
    def fetchAllVMData(self):
        print("VM DATA: ")
        try:
            row = self.connection.execute('select * from VM')
            VMList = list(row)
            return VMList
        except pyodbc.DatabaseError as err:
            print("Error Occurred while fetching VM Details", err)
            return None
        finally:
            self.connection.close()

    def GetAllVMsForThisUser(self, UniqueiD):
        cursor = connection.connections().getConnection()
        cursor.execute("SELECT * FROM VM")  # VM Table name
        usersList = LogIn.LogeIn().AllUsers()
        for i in usersList:
            if (i[2] == UniqueiD):
                conn = pyodbc.connect(
                    'Driver={ODBC Driver 17 for SQL Server}; SERVER=HP; Database=VM;Trusted_Connection=yes')
                SQLCommand = "SELECT [VMID], [Name], [VMIP], [OS], [LifeTime], [Owner], [Designation],[UniqueiD] FROM VM;"
                return SQLCommand
            else:
                return None

    def InsertVMData(self, Name, VMIP, OS, LifeTime, Owner, Designation, UniqueiD):
        cursor = connection.connections().getConnection()
        print('Inserting a new row into table')
        SQLTASK = ("INSERT INTO VM(Name, VMIP, OS, LifeTime, Owner, Designation,UniqueiD) VALUES (?,?,?,?,?,?,?)")
        with cursor.execute(SQLTASK, Name, VMIP, OS, LifeTime, Owner, Designation, UniqueiD):
            print('Successfully Inserted!')

    def UpdateVMData(self, Name, VMIP, OS, LifeTime, Owner, Designation, UniqueiD):
        cursor = connection.connections().getConnection()
        print('Updating Virtual Machine DataBase...')
        SQLTASK = (
            "UPDATE VM SET(Name, VMIP, OS, LifeTime, Owner, Designation,UniqueiD)=? WHERE VALUES = (?,?,?,?,?,?,?)")
        with cursor.execute(SQLTASK, Name, VMIP, OS, LifeTime, Owner, Designation, UniqueiD):
            print('Successfully Updated!')

    def deleteFromVMDB(self, VMID):
        cursor = connection.connections().getConnection()
        print('Deleting From Vertual Machines Data Base')
        SQLTASK = "DELETE FROM VM WHERE VMID = ?"
        with cursor.execute(SQLTASK, VMID):
            print('Successfully Deleted!')

    def readingFromVMDB(self):
        cursor = connection.connections().getConnection()
        print('Reading data from VM DATABASE table')
        SQLTASK = "SELECT VMID, Name FROM VM;"
        with cursor.execute(SQLTASK):
            row = cursor.fetchone()
            while row:
                print(str(row[0]) + " " + str(row[1]))
                row = cursor.fetchone()

    def Search(self, VMName):
        conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server}; SERVER=HP; Database=VM;Trusted_Connection=yes')
        SQLCommand = "SELECT [VMID], [Name], [VMIP], [OS], [LifeTime], [Owner], [Designation],[UniqueiD] FROM VM;"
        df = pd.read_sql(SQLCommand, conn)
        print("VM From Beginnig:   \n", df.head(2))
        print("\n\nVM From End:    \n", df.tail(1))
    def ExtendLifeTime(self, PassWord, VMName):
        ListOfUniqueiD = []
        ListOfAllVMs = []
        if (LogIn.LogeIn().CheckLogIn('root', PassWord)):
            listUsers = LogIn.LogeIn().AllUsers()
            for i in listUsers:
                ListOfUniqueiD.append(i[2])
        ListOfAllVMs = self.fetchAllVMData()
        for i in ListOfAllVMs:
            for j in ListOfUniqueiD:
                if (i[8] == j and VMName == i[1]):#not 100% if it i[8] =? i[5]=?
                    i[5]=i[5]+timedelta(days=30)

          #  for j in ListOfUniqueiD:
             #   VMExtemd = self.GetAllVMsForThisUser(j)  # list of data to single vm
            # for k in VMExtemd:
             # k[5] =k[5]+ timedelta(days=30)#k[5] ==> Life Time
            # self.GetAllVMsForThisUser()
            # listUsers[2]==> UniqueiD
    # ExtendedTime=LifeTime+ timedelta(days=30)



VMD = VMDB()
VMD.InsertVMData('MKo', '262534', 'xp', 30, '', '', '')
VMD.ExtendLifeTime('root', 'MKo')
# List435=[]
# VMD.Search()

# print(VMD.fetchAllVMData())
# print("=================================================")
