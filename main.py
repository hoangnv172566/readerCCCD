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
    try:
        icReaderWrappers.connect()
        icReaderWrappers.read_citizen_info()
        return icReaderWrappers.current_info.toJson()
    except Exception as e:
        return {"error": str(e)}
    
    
