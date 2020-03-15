import pyodbc
import connection
import pandas as pd
#######################



class VMDB:
    connection=connection.connections().getConnection()
    #cursor = connection.connections().getCursor()


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




    def InsertVMData(self, Name, VMIP, OS, LifeTime, Owner, Designation):
       # self.cursor = connection.connections().getCursor()
        #self.SQLCommand = ("INSERT INTO VM(Name, VMIP, OS, LifeTime, Owner, Designation) VALUES (?,?,?,?,?,?)")
        #self.Values = [Name, VMIP, OS, LifeTime, Owner,  Designation]
        #self.cursor.execute(self.SQLCommand, self.Values)
        #self.connection.commit()
        #print("Data Successfully Inserted")
        #self.connection.close()



       cursor = connection.connections().getConnection()
       print('Inserting a new row into table')
       SQLTASK = ("INSERT INTO VM(Name, VMIP, OS, LifeTime, Owner, Designation) VALUES (?,?,?,?,?,?)")
       with cursor.execute(SQLTASK, Name, VMIP, OS, LifeTime, Owner, Designation ):
           print('Successfully Inserted!')




    def UpdateVMData(self, Name, VMIP, OS, LifeTime, Owner, Designation):
        cursor = connection.connections().getConnection()
        print('Updating Virtual Machine DataBase...')
        SQLTASK = ("UPDATE VM SET(Name, VMIP, OS, LifeTime, Owner, Designation)=? WHERE VALUES = (?,?,?,?,?,?)")
        with cursor.execute(SQLTASK, Name, VMIP, OS, LifeTime, Owner, Designation):
            print('Successfully Updated!')



    def deleteFromVMDBbyID(self, VMID):
        cursor = connection.connections().getConnection()
        print('Deleting From Vertual Machines Data Base')
        SQLTASK = "DELETE FROM VM WHERE VMID = ?"
        with cursor.execute(SQLTASK, VMID):
            print('Successfully Deleted!')


    def deleteFromVMDBbyName(self, Name):
        cursor = connection.connections().getConnection()
        print('Deleting From Vertual Machines Data Base')
        SQLTASK = "DELETE FROM VM WHERE Name = ?"
        with cursor.execute(SQLTASK, Name):
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




    def Search(self):
        conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server}; SERVER=Amin\SQLEXPRESS; Database=VM;Trusted_Connection=yes')
        SQLCommand = "SELECT [VMID], [Name], [VMIP], [OS], [LifeTime], [Owner], [Designation] FROM VM;"
        df = pd.read_sql(SQLCommand, conn)
        print("VM From Beginnig:   \n",df.head(2))
        print("\n\nVM From End:    \n",df.tail(1))








VMD=VMDB()
#VMD.Search()
VMD.InsertVMData('XP',12345678,'XP',100,'AAAA','IT')
print(VMD.fetchAllVMData())







