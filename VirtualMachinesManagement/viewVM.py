from vmwc import VMWareClient

# view_vm_by_name:
def view_vm_by_name(host, username, password):
    status = 0
    with VMWareClient(host, username, password) as client:
        for vm in client.get_virtual_machines():
            print("VM name:",vm.name)
            status = 1

    if status != 1 :
        print("No virtual machines were found with this name!!!")