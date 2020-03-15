import pyodbc


class connections:
    def getConnection(self):
        conn = pyodbc.connect('Driver={SQL Server};Server=Amin\SQLEXPRESS;Database=VM;Trusted_Connection=yes;')
        print("Connection Successfully Established")
        return conn

    def getCursor(self):
        conn = pyodbc.connect('Driver={SQL Server};Server=Amin\SQLEXPRESS;Database=VM;Trusted_Connection=yes;')
        print("Connection Successfully Established")
        cursor = conn.cursor()
        return cursor
