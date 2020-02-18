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
            if(((hardware.cpuInfo.hz / 1000000)-(cpuUsage/1000))<rcpu):#TODO
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

    def DeleteVM(self,si, vmip):
        # delete vm from esxi
        VM = None
        VM = si.content.searchIndex.FindByIp(None, vmip, True)
        if VM == None:
            raise SystemExit("Unable to locate VirtualMachine.")
            return False

        else:
            print("Found: {0}".format(VM.name))
            print("The current powerState is: {0}".format(VM.runtime.powerState))
            if format(VM.runtime.powerState) == "poweredOn":
                print("Attempting to power off {0}".format(VM.name))
                TASK = VM.PowerOffVM_Task()
                tasks.wait_for_tasks(si, [TASK])
                print("{0}".format(TASK.info.state))

            print("Destroying VM from vSphere.")
            TASK = VM.Destroy_Task()
            tasks.wait_for_tasks(si, [TASK])
            print("Done.")
            return True

    # **********************************************************************

    def VMExistInEsxi(self,si, UuidVMs):
        # checking if all vm are existing in esxi
        # and return status per every vm
        statusVM = list()
        for i in UuidVMs:
            VM = None
            VM = si.content.searchIndex.FindByUuid(None, i, True, False)
            if VM == None:
                arr = [i, False]
            else:
                arr = [i, True]

            statusVM.append(arr)
        return statusVM











