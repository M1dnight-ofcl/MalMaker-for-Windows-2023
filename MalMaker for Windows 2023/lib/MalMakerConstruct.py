# Import PyQt5 Modules
from sre_constants import RANGE
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUi

# Import Modules
import sys
from datetime import datetime
from threading import Thread
from re import search

# Local Libraries
from lib.MalMakerLib import MalMakerEventScripts as mmlib

class constructToProprietaryMalFile:
    def __init__(self, eventList, eventParams, filename):
        print(f'| - constructToProprietaryMalFile [info] attempting to create file {filename}.mal')
        super().__init__()
        events = [eventList.item(eventIndex).text() for eventIndex in range(eventList.count())]
        print(f'| - constructToProprietaryMalFile [info] found events: {events} with params: {eventParams}')
        try:
            with open(f'{filename}.mal', 'x') as file:
                fileHeader = \
                f"""
                # --------------------------------------------------
                # fn:{filename}.mal - dt:{datetime}
                # raw data:
                {eventList}
                {eventParams}
                # --------------------------------------------------
                """
                fileContents = ''
                for event in events:
                    fileContents = fileContents + f"{event.split('_', 1)[0]}({str(eventParams[event.split('_', 1)[1]]).removeprefix('[').removesuffix(']')})\n"
                file.write(f'{fileHeader}\n{fileContents}')
                file.close()
                print(f'| - constructToProprietaryMalFile [info] made new file {filename}.mal with contents:\n{fileContents}')
        except Exception as e:
            print(f"| - constructToProprietaryMalFile [error] couldn't create file {filename}.mal because of exception:\n{e}")


class constructToGlobalExecutableFile:
    def __init__(self, eventList, filename):
        super().__init__()