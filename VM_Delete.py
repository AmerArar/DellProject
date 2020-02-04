from vmwc import VMWareClient

# delete_vm_by_name:
def delete_vm_by_name(host, username, password):
    with VMWareClient(host, username, password) as client:
        for vm in client.get_virtual_machines():
            if vm.name == "ubuntu64_new":
                vm.delete()
                print("Deleted VM")
        print("No virtual machines were found with this name!!!")