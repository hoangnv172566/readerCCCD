import os
from ctypes import *
import clr
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from io import BytesIO
from src.models.citizen_model import CitizenInfo

# Load the .NET assembly
libPath = os.getcwd() + '\\readerLibs\\FPTIDReaderSDK.dll'
clr.AddReference(libPath)

# Import namespaces from the .NET assembly
from FPT_IDReader_SDK import *
from FPT_IDReader_SDK.SmartCard.ICAO import *
from FPTIDReaderSDK.Extentions import *
from FPTIDReaderSDK.MRZ import *
from src.models.citizen_model import CitizenInfo

# Initialize cores
smartCardCore = SmartCardCore.GetInstance()
mrzCore = MRZCore.GetInstance()



class ICReaderWrappers:
    def __init__(self):
        super().__init__()
        
        # reader info
        self.l_smart_cards = None
        self.l_mrz_ports = None
        
        # flags
        self.card_absent_flags = True
        self.current_info = CitizenInfo()

    def find_readers(self):
        self.l_smart_cards = smartCardCore.GetListSmartCard()
        self.l_mrz_ports = mrzCore.GetListPort()
        
        self.l_smart_cards = [smc for smc in self.l_smart_cards]
        self.l_mrz_ports = [cmp for cmp in self.l_mrz_ports]
        

    def connect(self):
        # try:
        self.find_readers()
        
        if (self.l_smart_cards is not None) and (len(self.l_smart_cards) != 0):
            smartCardCore.SmartCard = self.l_smart_cards[0]
        
        if (self.l_mrz_ports is not None) and (len(self.l_mrz_ports) != 0):
            mrzCore.Port = self.l_mrz_ports[0]
                
        # except Exception as e:
        #     print("Error at connect: ", e)
    
    def read_citizen_info(self):
        if smartCardCore.IsCardAbsent:
            self.card_absent_flags = True
            return
        
        print("Reading Citizen Info")
        self.card_absent_flags = False
        
        try:
            icao_service = ICAOService()
            proccess_result = icao_service.ReadAll(True)
            
            if proccess_result.Status == ProccessResult.ProccessStatus.SUCCESS:
                self.current_info.fromCardData(proccess_result.CitizenInfo)
                print("Finished")
            else:
                print(f"{proccess_result.Code} - {proccess_result.Message}")
        except Exception as e:
            print("Error - ", e)
                   
            
