from io import BytesIO
from src.models.citizen_model import CitizenInfo

# Load the .NET assembly
import os
import clr
libPath = os.getcwd() + '\\readerLibs\\FPTIDReaderSDK.dll'
clr.AddReference(libPath)

# Import namespaces from the .NET assembly
from FPT_IDReader_SDK import *
from FPT_IDReader_SDK.SmartCard.ICAO import *
from FPTIDReaderSDK.Extentions import *
from FPTIDReaderSDK.MRZ import *
from src.models.citizen_model import CitizenInfo
from tkinter import *
from tkinter import ttk
from PIL import Image

smartCardCore = SmartCardCore.GetInstance()
mrzCore = MRZCore.GetInstance()

class CitizenViewModel:
    def __init__(self):
        self.title = ""
        self.content = ""

    def update_content(self, citizen_info):
        self.title = citizen_info.Title
        self.content = citizen_info.Content

    def clear_content(self):
        self.title = ""
        self.content = ""

class MainWindow(Tk):
    def __init__(self):
        super().__init__()
        self.view_model = CitizenViewModel()
        self.title("Main Window")
        self.geometry("600x400")

        self.smart_card_combobox = ttk.Combobox(self)
        self.smart_card_combobox.grid(row=0, column=0)
        self.smart_card_combobox.bind("<<ComboboxSelected>>", self.smart_card_selection_changed)

        self.mrz_combobox = ttk.Combobox(self)
        self.mrz_combobox.grid(row=0, column=1)
        self.mrz_combobox.bind("<<ComboboxSelected>>", self.mrz_selection_changed)

        self.fid_reader_button = Button(self, text="FID Reader", command=self.fid_reader_button_click)
        self.fid_reader_button.grid(row=1, column=0)

        self.test_button = Button(self, text="Test", command=self.test_button_click)
        self.test_button.grid(row=1, column=1)

        self.clear_button = Button(self, text="Clear", command=self.clear_button_click)
        self.clear_button.grid(row=1, column=2)

        self.test_all_button = Button(self, text="Test All", command=self.test_all_button_click)
        self.test_all_button.grid(row=1, column=3)

        self.status_text = Label(self, text="")
        self.status_text.grid(row=2, column=0, columnspan=4)

        self.citizen_image_label = Label(self)
        self.citizen_image_label.grid(row=3, column=0, columnspan=4)

        self.data_verify_text = Text(self, height=10, width=50)
        self.data_verify_text.grid(row=4, column=0, columnspan=4)

    def fid_reader_button_click(self):
        smartcards = smartCardCore.GetListSmartCard()
        mrz_list = mrzCore.GetListPort()
        self.smart_card_combobox['values'] = [smartcard for smartcard in smartcards]
        self.mrz_combobox['values'] = [mrz for mrz in mrz_list]
      
        

    def smart_card_selection_changed(self, event):
        if self.smart_card_combobox.get():
            smartCardCore.SmartCard = self.smart_card_combobox.get()

    def test_button_click(self):
        if smartCardCore.IsCardAbsent:
            self.status_text['text'] = "Card Absent"
            return
        self.status_text['text'] = "STARTING"
        icao_service = ICAOService()
        proccess_result = icao_service.Read("025099004422", False)
        if proccess_result.Status == ProccessResult.ProccessStatus.SUCCESS:
            # self.view_model.update_content(proccess_result.CitizenInfo)
            # print(proccess_result.CitizenInfo.ToString())
            image = Image.open(BytesIO(proccess_result.CitizenInfo.PhotoBytes))
            image.thumbnail((80, 110))
            photo = ImageTk.PhotoImage(image)
            self.citizen_image_label.config(image=photo)
            self.citizen_image_label.image = photo
            self.data_verify_text.delete(1.0, END)
            self.data_verify_text.insert(END, proccess_result.CitizenInfo.DataVerify.ToStringJsonPretty())
            self.status_text['text'] = "DONE"
        else:
            self.status_text['text'] = f"{proccess_result.Code} - {proccess_result.Message}"
        

    def clear_button_click(self):
        self.status_text['text'] = ""
        self.view_model.clear_content()
        self.citizen_image_label.config(image='')
        self.data_verify_text.delete(1.0, END)

    def test_all_button_click(self):
        if smartCardCore.IsCardAbsent:
            self.status_text['text'] = "Card Absent"
            print("Card Absent")
            return
        self.status_text['text'] = "STARTING"
        print("starting")
        
        icao_service = ICAOService()
        proccess_result = icao_service.ReadAll(True)
        print(proccess_result.Status)
        if proccess_result.Status == ProccessResult.ProccessStatus.SUCCESS:
            # self.view_model.update_content(proccess_result.CitizenInfo)
            image = Image.open(BytesIO(proccess_result.CitizenInfo.PhotoBytes))
            image.thumbnail((80, 110))
            photo = ImageTk.PhotoImage(image)
            self.citizen_image_label.config(image=photo)
            self.citizen_image_label.image = photo
            self.data_verify_text.delete(1.0, END)
            citizenInfo = proccess_result.CitizenInfo
            # dataVerify = citizenInfo.DataVerify
            self.data_verify_text.insert(END, citizenInfo.ToString())
            self.status_text['text'] = "DONE"
        else:
            self.status_text['text'] = f"{proccess_result.Code} - {proccess_result.Message}"
       

    def mrz_selection_changed(self, event):
        if self.mrz_combobox.get():
            mrzCore.Port = self.mrz_combobox.get()

import signal
if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    mw = MainWindow()
    mw.mainloop()
    