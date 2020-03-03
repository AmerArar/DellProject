import datetime
import pyVmomi
import pyVim
from flask import jsonify
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi.SoapAdapter import CONNECTION_POOL_IDLE_TIMEOUT_SEC
import ssl
from vmwc import VMWareClient

from Manage_Virtual_Machines.VirtualMachinesManagement import ConnectTOserver, viewVM, VM_Delete
from Manage_Virtual_Machines.VirtualMachinesManagement.CRT import CreateVMtoEsxi
from Manage_Virtual_Machines.VirtualMachinesManagement.management import Management

import http.server
import socketserver

#################Server#################################

from http.server import BaseHTTPRequestHandler, HTTPServer
import time

hostName = "localhost"
serverPort = 8080

class MyServer(BaseHTTPRequestHandler):
    REStest=50

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")

        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')

        self.end_headers()
        self.wfile.write(bytes("[{\"userId\": \"1\",\"id\": \"1\",\"title\": \"suntt\",\"body\": \"quia et suscipit\"}]", "utf-8"))

#######################################################



def Main():
    print("begin")
#///////////////////////////////////
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
#///////////////////////
    # num=0
    # #Connect TO server:
    # ConnectTOserver.ConnectTOserver()
    # while (num < 5):
    #     print("---------------------------------------------------")
    #     print("-- To create a virtual machine press 1           --")
    #     print("-- To view all virtual machines By User press 2  --")
    #     print("-- To delete a virtual machine 3                 --")
    #     print("-- To view available resources, press 4          --")
    #     print("-- To Exit , Press another key                   --")
    #     print("---------------------------------------------------")
    #     num = int(input())
    #
    #     # CreateVM:
    #     if num == 1:
    #         # C=Management("vm457", "10.0.0.1", "XP", "on",'1024', '15','30')
    #         # print(C)
    #         C=CreateVMtoEsxi("root", "192.168.174.139","Amer2020@" , "vm3", 2, 2024, 9)
    #
    #     else:
    #         # view all VM By User:
    #         if num == 2:
    #             viewVM.view_vm_by_name("192.168.174.139", "root", "Amer2020@")
    #
    #         else:
    #             # Delet vm_by name:
    #             if num == 3:
    #                 Name = input("Type a virtual machine name to delete : ")
    #                 VM_Delete.delete_vm_by_name("192.168.174.139", "root", "Amer2020@", Name)
    #
    #             else:
    #                 #view available resources:
    #                 if num == 4:
    #                     print("Resources TO DO!!")
    #
    #                 else:
    #                     # Exit:
    #                     break
    #
    #

    print("end")

Main()
