import pyodbc
import connection
import pandas as pd



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
        self.cursor = connection.connections().getConnection()
        SQLCommand = ("INSERT INTO VM(Name, VMIP, OS, LifeTime, Owner, Designation) VALUES (?,?,?,?,?,?)")
        Values = [Name, VMIP, OS, LifeTime, Owner,  Designation]
        self.cursor.execute(SQLCommand, Values)
        self.connection.commit()
        print("Data Successfully Inserted")
        self.connection.close()






    def Search(self):
        sql_conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server}; SERVER=Amin\SQLEXPRESS; Database=VM;Trusted_Connection=yes')
        SQLCommand = "SELECT [VMID], [Name], [VMIP], [OS], [LifeTime], [Owner], [Designation] FROM VM;"
        df = pd.read_sql(SQLCommand, sql_conn)
        print("VM From Beginnig:   \n",df.head(2))
        print("\n\nVM From End:    \n",df.tail(1))





VMD=VMDB()
#VMD.Search()
#VMD.InsertVMData('XP',12345678,'XP',100,'AAAA','IT')
print(VMD.fetchAllVMData())






