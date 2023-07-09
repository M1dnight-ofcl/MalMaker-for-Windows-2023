# Import PyQt5 Modules
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUi
from pyautogui import press, typewrite, hotkey

# Import Modules
import sys, os
from threading import Thread

class MalMakerEventScripts:
    def __init__(self):
        super(MalMakerEventScripts, self).__init__()

    def openDialogEvent(title:str="malmaker popup", message:str="this is a malmaker popup that has not been configured"):
        print('[info] creating new dialog')
        newDialog = QDialog()
        newDialogLayout = QVBoxLayout()
        newDialog.setWindowTitle(f'{title}')
        newDialogMessage = QLabel(f'{message}')
        newDialogLayout.addWidget(newDialogMessage)
        newDialog.setLayout(newDialogLayout)
        newDialog.exec_()

    def newFileEvent(fileName:str='new-malmaker-file', path:str='', fileContents:str=''):
        print(f'| - newFileEvent() [info] attempting to create new file at {path}{fileName}')
        try:
            with open(f'{path}{fileName}', 'x') as newFile:
                newFile.write(f'{fileContents}')
                newFile.close()
            print(f'| - newFileEvent() [info] created new file at {path}{fileName}')
        except:
            print(f'| - newFileEvent() [info] failed to create file at {path}{fileName}, already exists')

    def sendKey(key):
        press(key)