import ssl
import math
from asyncio import tasks
from cgi import log
from pyVim import connect
from pyVim.connect import SmartConnect
from pyVmomi import vim, vmodl
MBFACTOR = float(1 << 20) #MB
class ManageESXI:
    def CheckResourc(self,host, rcpu, rmemoryGB, rspaceGB, datastore):
        #host: HostSystem obj
        #datastore: Datastore obj
        #rcpu,rmemoryGB, rspaceGB: The resource required for VM
        try:
            summary = host.summary
            stats = summary.quickStats
            hardware = host.hardware
            cpuUsage = stats.overallCpuUsage
            if(((hardware.cpuInfo.hz / 1000000)-(cpuUsage/1000))<rcpu):
                #Calculate the CPU number available for this host
                return False
            memoryCapacityInMB = hardware.memorySize / MBFACTOR
            memoryCapacityGB = memoryCapacityInMB / 1024
            memoryUsage = (stats.overallMemoryUsage) / 1024
            if ((math.ceil(memoryCapacityGB) - memoryUsage) < rmemoryGB):
                return False
        except Exception as error:
            print("Unable to access information for host: ", host.name)
            print(error)

        try:
            summary = datastore.summary
            freeSpaceMB = summary.freeSpace / MBFACTOR
            if ((freeSpaceMB / 1024) < rspaceGB):
                return False
        except Exception as error:
            print("Unable to access summary for datastore: ", datastore.name)
            print(error)

        return True
    def GetManagedObject(self,content, vimtype):
        # Return an object by type
        return [item for item in content.viewManager.CreateContainerView(content.rootFolder, [vimtype], recursive=True).view]

    def GetObj(self,content, vimtype, name):
        """
               Return an object by name, if name is None the
               first found object is returned
               """
        obj = None
        container = content.viewManager.CreateContainerView(content.rootFolder, vimtype, True)
        for c in container.view:
            if name:
                if c.name == name:
                    obj = c
                    break
            else:
                obj = c
                break

        return obj

    def Delete(self,vm, content):
        if isinstance(vm, str):
            vm = self.GetObj(content, [vim.VirtualMachine], vm)
        if (vm == None):
            print("There is no machine with that name")
            return False
        else:
            print("Found: {0}".format(vm.name))
            print("The current powerState is: {0}".format(vm.runtime.powerState))
            if format(vm.runtime.powerState) == "poweredOn":
                print("Attempting to power off {0}".format(vm.name))
                TASK = vm.PowerOffVM_Task()
                # wait_for_tasks( [TASK])
                print("{0}".format(TASK.info.state))

            print("Destroying VM from vSphere.")
            vm.Destroy_Task()
            # wait_for_tasks( [TASK])
            print("Done.")
            return True
        # Method that populates objects of type vimtype

    def GetAllObjs(self,content, vimtype):
        obj = {}
        container = content.viewManager.CreateContainerView(content.rootFolder, vimtype, True)
        for managed_object_ref in container.view:
            obj.update({managed_object_ref: managed_object_ref.name})
        return obj

    def Get_All_VM(self,content):
        virtual_machines = self.GetAllObjs(content, [vim.VirtualMachine])
        if (len(virtual_machines) < 1):
            print("There are no virtual machines for this host")
            return None
        else:
            _virtual_machines = {}

            for vm in virtual_machines:
                _ip_address = ""
                summary = vm.summary
                if summary.guest is not None:
                    _ip_address = summary.guest.ipAddress
                    if _ip_address is None:
                        _ip_address = ""

                virtual_machine = {
                    summary.config.name: {
                        "guest_fullname": summary.config.guestFullName,
                        "power_state": summary.runtime.powerState,
                        "ip_address": _ip_address
                    }
                }

                _virtual_machines.update(virtual_machine)
            return _virtual_machines















