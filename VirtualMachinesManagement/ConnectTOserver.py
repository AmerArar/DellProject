from vmwc import VMWareClient

class ConnectTOserver():
    def __init__(self):
        host = '192.168.174.139'
        username = 'root'
        password = 'amer1234'
        with VMWareClient(host, username, password) as client:
            print("The ESXI connection was successful")
