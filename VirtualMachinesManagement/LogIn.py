import pyodbc
import pandas as pd
import uuid
class LogeIn:
    def CreatNewUser(self,UserName,PassWord):
        conn = pyodbc.connect(Driver='{SQL Server}', Server='HP', Database='LogIn', Trusted_Connection='yes')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM LogIn')
        UniqueiD="todo"
        SQLTASK = ("INSERT INTO LogIn(UserName,PassWord,UniqueiD) VALUES (?,?,?)")
        with cursor.execute(SQLTASK, UserName, PassWord, UniqueiD):
            print('Successfully Inserted!')
        conn.commit()
        conn.close()
    def AllUsers(self):
        c= pyodbc.connect(Driver='{SQL Server}', Server='HP', Database='LogIn', Trusted_Connection='yes')
        userList = []
        try:
            row = c.execute('select * from LogIn')
            userList = list(row)
            # print(userList)
        except pyodbc.DatabaseError as err:
            print("Error Occurred while fetching VM Details", err)
            print(None)
        finally:
            c.close()
        return userList
    def CheckLogIn(self, UserName, PassWord):
        conn = pyodbc.connect(Driver='{SQL Server}', Server='HP', Database='LogIn', Trusted_Connection='yes')
        usersList=self.AllUsers()
        for i in usersList:
            if(i[0]==UserName and i[1]==PassWord):
                return True
            else:
                return False

