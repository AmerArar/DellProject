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
#***************************************************************************************************
    def get_args(self):
        parser = argparse.ArgumentParser(description='Arguments for talking to vCenter')

        parser.add_argument('-s', '--host',
                            required=True,
                            action='store',
                            help='vSpehre service to connect to')

        parser.add_argument('-o', '--port',
                            type=int,
                            default=443,
                            action='store',
                            help='Port to connect on')

        parser.add_argument('-u', '--user',
                            required=True,
                            action='store',
                            help='Username to use')

        parser.add_argument('-p', '--password',
                            required=False,
                            action='store',
                            help='Password to use')

        parser.add_argument('-v', '--vm-name',
                            required=True,
                            action='store',
                            help='Name of the VM you wish to make')

        parser.add_argument('--no-ssl',
                            action='store_true',
                            help='Skip SSL verification')

        parser.add_argument('--template',
                            required=True,
                            action='store',
                            help='Name of the template/VM \
                                you are cloning from')

        parser.add_argument('--datacenter-name',
                            required=False,
                            action='store',
                            default=None,
                            help='Name of the Datacenter you\
                                wish to use. If omitted, the first\
                                datacenter will be used.')

        parser.add_argument('--vm-folder',
                            required=False,
                            action='store',
                            default=None,
                            help='Name of the VMFolder you wish\
                                the VM to be dumped in. If left blank\
                                The datacenter VM folder will be used')

        parser.add_argument('--datastore-name',
                            required=False,
                            action='store',
                            default=None,
                            help='Datastore you wish the VM to end up on\
                                If left blank, VM will be put on the same \
                                datastore as the template')

        parser.add_argument('--datastorecluster-name',
                            required=False,
                            action='store',
                            default=None,
                            help='Datastorecluster (DRS Storagepod) you wish the VM to end up on \
                                Will override the datastore-name parameter.')

        parser.add_argument('--cluster-name',
                            required=False,
                            action='store',
                            default=None,
                            help='Name of the cluster you wish the VM to\
                                end up on. If left blank the first cluster found\
                                will be used')

        parser.add_argument('--resource-pool',
                            required=False,
                            action='store',
                            default=None,
                            help='Resource Pool to use. If left blank the first\
                                resource pool found will be used')

        parser.add_argument('--power-on',
                            dest='power_on',
                            action='store_true',
                            help='power on the VM after creation')

        parser.add_argument('--opaque-network',
                            required=False,
                            help='Name of the opaque network to add to the VM')

        args = parser.parse_args(
            ['-s', "192.168.75.128", '-u', "root", '-p', "", '-v', "vmmmm1"])

        if not args.password:
            args.password = getpass.getpass(
                prompt='Enter password')

        return args

    def wait_for_task(self,task):
        """ wait for a vCenter task to finish """
        task_done = False
        while not task_done:
            if task.info.state == 'success':
                return task.info.result

            if task.info.state == 'error':
                print("there was an error")

    def clone_vm(self, content, template, vm_name, si, datacenter_name, vm_folder, datastore_name, cluster_name, resource_pool, power_on, datastorecluster_name):
        """
        Clone a VM from a template/VM, datacenter_name, vm_folder, datastore_name
        cluster_name, resource_pool, and power_on are all optional.
        """

        # if none git the first one
        datacenter = get_obj(content, [vim.Datacenter], datacenter_name)

        if vm_folder:
            destfolder = get_obj(content, [vim.Folder], vm_folder)
        else:
            destfolder = datacenter.vmFolder

        if datastore_name:
            datastore = get_obj(content, [vim.Datastore], datastore_name)
        else:
            datastore = get_obj(
                content, [vim.Datastore], template.datastore[0].info.name)

        # if None, get the first one
        cluster = get_obj(content, [vim.ClusterComputeResource], cluster_name)

        if resource_pool:
            resource_pool = get_obj(content, [vim.ResourcePool], resource_pool)
        else:
            resource_pool = cluster.resourcePool

        vmconf = vim.vm.ConfigSpec()

        if datastorecluster_name:
            podsel = vim.storageDrs.PodSelectionSpec()
            pod = get_obj(content, [vim.StoragePod], datastorecluster_name)
            podsel.storagePod = pod

            storagespec = vim.storageDrs.StoragePlacementSpec()
            storagespec.podSelectionSpec = podsel
            storagespec.type = 'create'
            storagespec.folder = destfolder
            storagespec.resourcePool = resource_pool
            storagespec.configSpec = vmconf

            try:
                rec = content.storageResourceManager.RecommendDatastores(
                    storageSpec=storagespec)
                rec_action = rec.recommendations[0].action[0]
                real_datastore_name = rec_action.destination.name
            except:
                real_datastore_name = template.datastore[0].info.name

            datastore = get_obj(content, [vim.Datastore], real_datastore_name)

        # set relospec
        relospec = vim.vm.RelocateSpec()
        relospec.datastore = datastore
        relospec.pool = resource_pool

        clonespec = vim.vm.CloneSpec()
        clonespec.location = relospec
        clonespec.powerOn = power_on

        print("cloning VM...")
        task = template.Clone(folder=destfolder, name=vm_name, spec=clonespec)
        wait_for_task(task)










