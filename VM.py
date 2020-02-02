from adles import utils
from adles.vsphere.folder_utils import find_in_folder
class VM:
    """ Represents a VMware vSphere Virtual Machine instance.
    .. warning::    You must call :meth:`create` if a vim.VirtualMachine object
                    is not used to initialize the instance.
    """

    def __init__(self, vm=None, name=None, folder=None, resource_pool=None,
                 datastore=None, host=None):
        """
        :param vm: VM instance to use instead of calling :meth:`create`
        :type vm: vim.VirtualMachine
        :param str name: Name of the VM
        :param folder: Folder in inventory to create the VM in
        :type folder: vim.Folder
        :param resource_pool: Resource pool to use for the VM
        :type resource_pool: vim.ResourcePool
        :param datastore: Datastore the VM is stored on
        :type datastore: vim.Datastore
        :param host: Host the VM runs on
        :type host: vim.HostSystem
        """
        self._log = logging.getLogger('VM')
        if vm is not None:
            self._vm = vm
            self.name = vm.name
            self.folder = vm.parent
            self.resource_pool = vm.resourcePool
            #self.datastore = vm.datastore[0]
            self.datastore = vm.datastore
            self.host = vm.summary.runtime.host
            self.network = vm.network
            self.runtime = vm.runtime
            self.summary = vm.summary
        else:
            self._vm = None
            self.name = name
            self.folder = folder  # vim.Folder that will contain the VM
            self.resource_pool = resource_pool  # vim.ResourcePool to use VM
            self.datastore = datastore  # vim.Datastore object to store VM on
            self.host = host  # vim.HostSystem

    def edit_resources(self, cpus=None, cores=None,
                       memory=None, max_consoles=None):
        """Edits the resource limits for the VM.
        :param int cpus: Number of CPUs
        :param int cores: Number of CPU cores
        :param int memory: Amount of RAM in MB
        :param int max_consoles: Maximum number of simultaneous
        Mouse-Keyboard-Screen (MKS) console connections
        """
        spec = vim.vm.ConfigSpec()
        if cpus is not None:
            spec.numCPUs = int(cpus)
        if cores is not None:
            spec.numCoresPerSocket = int(cores)
        if memory is not None:
            spec.memoryMB = int(memory)
        if max_consoles is not None:
            spec.maxMksConnections = int(max_consoles)
        self._edit(spec)

    def create(self, template=None, cpus=None, cores=None, memory=None,
      max_consoles=None, version=None, firmware='efi',  datastore_path=None):
        """Creates a Virtual Machine.
        :param vim.VirtualMachine template: Template VM to clone
        :param int cpus: Number of processors
        :param int cores: Number of processor cores
        :param int memory: Amount of RAM in MB
        :param int max_consoles: Maximum number of active console connections
        :param int version: Hardware version of the VM
        [default: highest host supports]
        :param str firmware: Firmware to emulate for the VM (efi | bios)
        :param str datastore_path: Path to existing VM files on datastore
        :return: If the creation was successful
        :rtype: bool
        """
        if template is not None:  # Use a template to create the VM
            self._log.debug("Creating VM '%s' by cloning %s",
                            self.name, template.name)
            clonespec = vim.vm.CloneSpec()
            clonespec.location = vim.vm.RelocateSpec(pool=self.resource_pool,
                                                     datastore=self.datastore)
            if not template.CloneVM_Task(folder=self.folder, name=self.name,
                                         spec=clonespec).wait(120):
                self._log.error("Error cloning VM %s", self.name)
                return False
        else:  # Generate the specification for and create the new VM
            self._log.debug("Creating VM '%s' from scratch", self.name)
            spec = vim.vm.ConfigSpec()
            spec.name = self.name
            spec.numCPUs = int(cpus) if cpus is not None else 1
            spec.numCoresPerSocket = int(cores) if cores is not None else 1
            spec.cpuHotAddEnabled = True
            spec.memoryMB = int(memory) if memory is not None else 512
            spec.memoryHotAddEnabled = True
            spec.firmware = str(firmware).lower()
            if version is not None:
                spec.version = "vmx-" + str(version)
            if max_consoles is not None:
                spec.maxMksConnections = int(max_consoles)
            vm_path = '[' + self.datastore[0].name + '] '
            if datastore_path:
                vm_path += str(datastore_path)
            vm_path += self.name + '/' + self.name + '.vmx'
            spec.files = vim.vm.FileInfo(vmPathName=vm_path)
            self._log.debug("Creating VM '%s' in folder '%s'",
                            self.name, self.folder.name)
            if not self.folder.CreateVM_Task(spec, self.resource_pool, self.host).wait():
                self._log.error("Error creating VM %s", self.name)
                return False

        self._vm = find_in_folder(self.folder, self.name,
                                  vimtype=vim.VirtualMachine)
        if not self._vm:
            self._log.error("Failed to make VM %s", self.name)
            return False
        self.network = self._vm.network
        self.runtime = self._vm.runtime
        self.summary = self._vm.summary
        if template is not None:  # Edit resources for a clone if specified
            self.edit_resources(cpus=cpus, cores=cores, memory=memory,
                                max_consoles=max_consoles)

        self._log.debug("Created VM %s", self.name)
        return True

    def _find_free_ide_controller(self,vm):
        """
        Finds a free IDE controller to use.
        :return: The free IDE controller
        :rtype: vim.vm.device.VirtualIDEController or None
        """
        for dev in vm.config.hardware.device:
            if isinstance(dev, vim.vm.device.VirtualIDEController) \
                    and len(dev.device) < 2:
                # If there are less than 2 devices attached, we can use it
                return dev
        return None

    def _edit(self, vm,config):
        """Reconfigures VM with the given configuration specification.
        :param vim.vm.ConfigSpec config: The configuration specification to apply
        :return: If the edit was successful
        """
        if not vm.ReconfigVM_Task(config).wait():
            self._log.error("Failed to edit VM %s", vm.name)
            return False
        else:
            return True

    def attach_iso(self, iso_path, datastore=None, boot=True,vm=None):
        """
        Attaches an ISO image to a VM.
        :param str iso_path: Path in the Datastore of the ISO image to attach
        :param vim.Datastore datastore: Datastore where the ISO resides
        [defaults to the VM's datastore]
        :param bool boot: Set VM to boot from the attached ISO
        """
        self._log.debug("Adding ISO '%s' to '%s'", iso_path, self.name)
        if datastore is None:
            datastore = self.datastore

        spec = vim.vm.device.VirtualDeviceSpec()
        spec.device = vim.vm.device.VirtualCdrom()
        spec.device.key = -1
        spec.device.unitNumber = 0

        # Find a disk controller to attach to
        controller = self._find_free_ide_controller(vm)
        #controller = "ubuntu-18.04.3-desktop-amd64.iso"
        if controller:
            spec.device.controllerKey = controller.key
        else:
            self._log.error("Could not find a free IDE controller "
                            "on '%s' to attach ISO '%s'",
                            self.name, iso_path)
            return

        spec.device.backing = vim.vm.device.VirtualCdrom.IsoBackingInfo()
        # Attach ISO
        spec.device.backing.fileName = "[%s] %s" % (datastore.name, iso_path)
        # Set datastore containing the ISO file
        spec.device.backing.datastore = datastore

        spec.device.connectable = vim.vm.device.VirtualDevice.ConnectInfo()
        # Allows guest OS to control device
        spec.device.connectable.allowGuestControl = True
        # Ensures ISO is connected at boot
        spec.device.connectable.startConnected = True

        spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.add
        vm_spec = vim.vm.ConfigSpec(deviceChange=[spec])
        if boot:  # Set the VM to boot from the ISO upon power on
            self._log.debug("Setting '%s' to boot from ISO '%s'",
                            self.name, iso_path)
            order = [vim.vm.BootOptions.BootableCdromDevice()]
            order.extend(list(vm.config.bootOptions.bootOrder))
            vm_spec.bootOptions = vim.vm.BootOptions(bootOrder=order)
        self._edit(vm,vm_spec)  # Apply change to VM

    def powered_on(self):
        """Determines if a VM is powered on.
        :return: If VM is powered on
        :rtype: bool
        """
        return self._vm.runtime.powerState == \
               vim.VirtualMachine.PowerState.poweredOn

    def destroy(self):
        """Destroys the VM."""
        self._log.debug("Destroying VM %s", self.name)
        if self.powered_on():
            self.change_state("off")
        self._vm.Destroy_Task().wait()

