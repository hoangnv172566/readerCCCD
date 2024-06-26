from ctypes import *
from tkinter import *
from wrapper import ICReaderWrappers
from fastapi import FastAPI
from dataclasses import asdict

app = FastAPI()

icReaderWrappers = ICReaderWrappers()

# Call the function
# @app.get("/check-connection")
# def check_connection():
#     return icReaderWrappers.check_current_status()


@app.get("/read-info")
def read_current_card():
    icReaderWrappers.connect()

    print(icReaderWrappers.l_smart_cards[0])
    # print(icReaderWrappers.l_mrz_ports[0])
    icReaderWrappers.read_citizen_info()
    print(icReaderWrappers.current_info.toJson())
    
