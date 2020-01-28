from vmwc import VMWareClient
def CreateVM(username,host,password,vmname,numcpu,ramMB,disksizeGB):
    with VMWareClient(host, username, password) as client:
        vm = client.new_virtual_machine(vmname, cpus=numcpu, ram_mb=ramMB, disk_size_gb=disksizeGB)
        vm.configure_bios(boot_delay=5000, boot_order=['network', 'disk'])
        vm.power_on()


def main():
    CreateVM("root","192.168.253.128", "12345678", "tttt",2, 1024, 20)


if __name__ == '__main__':
    main()