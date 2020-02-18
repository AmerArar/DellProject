from vmwc import VMWareClient
import VMDBExpress01


# delete_vm_by_name:
def delete_vm_by_name(host, username, password,vmname):
    status = 0
    with VMWareClient(host, username, password) as client:
        for vm in client.get_virtual_machines():
            if vm.name == vmname :
                vm.delete()
                VMDBExpress01.VMDB().deleteFromVMDBbyName(vmname)
                status = 1
                print("Deleted VM")
    if status != 1 :
        print("No virtual machines were found with this name!!!")
