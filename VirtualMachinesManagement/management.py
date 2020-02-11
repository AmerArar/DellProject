class Management:
    def __init__(self, VMName, Ip, OperatingSystem, Status, Ram, Storage, LifeTime):
        self.VMName = VMName
        self.Ip = Ip
        self.OperatingSystem = OperatingSystem
        self.Status = Status
        self.Ram = Ram
        self.Storage = Storage
        self.LifeTime = LifeTime

    def CreateVM(self):
        pass

    def DeleteVM(self):
        pass

    def GetAllVMs(self):
        pass

    def ExtendVMLifeTime(self):
        pass