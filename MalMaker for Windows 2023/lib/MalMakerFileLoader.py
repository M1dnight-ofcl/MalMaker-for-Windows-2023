# Import PyQt5 Modules
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
from main import ScriptWindow

class openFile:
    def __init__(self):
        super(openFile, self).__init__()
        
        self.handleMalFileUpload(QFileDialog().getOpenFileName(caption='Open MalMaker Project', filter='MalMaker Projects (*.mal)'))

    def handleMalFileUpload(self, file):
        print(f'| - openFile.handleMalFileUpload() [info] got file {file[0]}')
        with open(file[0], 'r') as f:
            self.fileData = f.read()
            self.lines = self.fileData.split('\n')
            count = 0
            print(f'| - openFile.handleMalFileUpload() [info] data from file:\n{self.fileData}')
            print(f'| - openFile.handleMalFileUpload() [info] seperated lines of file: {self.lines}')
            for line in self.lines:
                count+=1
                if count in range(4):
                    print(f'| - openFile.handleMalFileUpload()::line-interpreter [info] skipped on line {count}')
                    pass
                if count == 5:
                    eventListContents = eval(line.split('=')[1])
                    print(f'| - openFile.handleMalFileUpload()::line-interpreter [info] got eventListContents: {eventListContents}')
                if count == 6:
                    eventParams = eval(line.split('=')[1])
                    print(f'| - openFile.handleMalFileUpload()::line-interpreter [info] got eventParams: {eventParams}')
                elif count >= 7:
                    print(f'| - openFile.handleMalFileUpload()::line-interpreter [info] skipped on line {count}')
                    pass
        ScriptWindow().loadInformation(eventListContents, eventParams)
