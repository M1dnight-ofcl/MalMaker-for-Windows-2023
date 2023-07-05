# MalMaker for Windows
# By M1dnightDev (c) 2023
#
# Icon Pack: https://www.iconarchive.com/show/refresh-cl-icons-by-tpdkdesign.net.1.html

# Import PyQt5 Modules
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUi

# Import Modules
import sys
from threading import Thread
from re import search

# Local Libraries
from lib import MalMakerLib as mmlib, \
                MalMakerConstruct as mmconst, \
                MalMakerFileLoader as mmfldr
	
class WelcomeWindow(QMainWindow):
    def __init__(self):
        super(WelcomeWindow, self).__init__()
        loadUi('ui/welcome.ui', self)

class messageConfigMenu(QDialog):
    def __init__(self, index, titlePlaceholder:str='', messagePlaceholder:str=''):
        super(messageConfigMenu, self).__init__()
        self.editMenu = loadUi('ui/messageConfigMenu.ui', self)
        self.setWindowTitle(f'Edit Object Parameters at Index {index}')

        self.confirm.clicked.connect(lambda: self.submitParams(index))
        
        self.messageTitle.setText(titlePlaceholder)
        self.messageContents.setText(messagePlaceholder)

        self.exec_()

    def submitParams(self, index):
        self.title = self.messageTitle.text()
        self.contents = self.messageContents.toPlainText()

        print(f'| - messageConfigMenu.submitParams [info] setting params for index {index}')

        paramLinkedToIndex[f'{index}'] = [self.title, self.contents]
        print(f'| - messageConfigMenu.submitParams [info] linked params: { paramLinkedToIndex[f"{index}" ]} to index {index}')
        self.close()

class newFileConfigMenu(QDialog):
    def __init__(self, index, filePath:str='', fileName:str='', fileContents:str=''):
        super(newFileConfigMenu, self).__init__()
        self.editMenu = loadUi('ui/newFileConfigMenu.ui', self)
        self.setWindowTitle(f'Edit Object Parameters at Index {index}')

        self.confirm.clicked.connect(lambda: self.submitParams(index))
        
        self.filePath.setText(filePath)
        self.fileName.setText(fileName)
        self.fileContents.setText(fileContents)

        self.exec_()

    def submitParams(self, index):
        self.file = self.fileName.text()
        self.path = self.filePath.text()
        self.contents = self.fileContents.toPlainText()

        print(f'| - newFileConfigMenu.submitParams [info] setting params for index {index}')

        paramLinkedToIndex[f'{index}'] = [self.path, self.file, self.contents]
        print(f'| - newFileConfigMenu.submitParams [info] linked params: { paramLinkedToIndex[f"{index}" ]} to index {index}')
        self.close()


class ScriptWindow(QMainWindow):
    def __init__(self):
        super(ScriptWindow, self).__init__()
        loadUi('ui/writeScript.ui', self)

        self.eventFunctionMapping()

        self.eventList.clicked.connect(self.getLastItem)

        self.paramEditMenu.clicked.connect(self.editParamsAtCurrentIndex)
        self.delete_2.clicked.connect(self.deleteAtCurrentIndex)

        self.addEvent.clicked.connect(self.addNewScript)
        self.runScriptButton.clicked.connect(self.runScript)

        def getFileName(): global file; file = self.fileName.text()
        getFileName()
        self.fileName.textChanged.connect(getFileName)

        self.save.clicked.connect(lambda: mmconst.constructToProprietaryMalFile(self.eventList, paramLinkedToIndex, file))
        

    def getLastItem(self):
        self.lastItem = self.eventList.currentItem()

    def addNewScript(self):
        self.currentSelectedEventType = self.eventType.currentText()
        self.index = self.eventList.count()
        print(f'[info] user requested event addition {self.currentSelectedEventType} at index {self.eventList.count()}')

        item = QListWidgetItem(f'{self.currentSelectedEventType}_{self.index}')
        self.eventList.addItem(item)
        self.paramMenu[f'{self.currentSelectedEventType}'](self.index)

    def eventFunctionMapping(self):
        global paramLinkedToIndex
        paramLinkedToIndex = {} # ex = index: [arg1, arg2, arg3+]
        self.paramMenu = \
        {
            "Open Dialog": messageConfigMenu,
               "New File": newFileConfigMenu,
        }
        self.eventMaps = \
        {
            "Open Dialog": mmlib.MalMakerEventScripts.openDialogEvent,
               "New File": mmlib.MalMakerEventScripts.newFileEvent,
        }


    def runScript(self, args:list=None):
        print(f'[info] script has been initialized')
        for EventIndex in range(self.eventList.count()):
            self.Event = self.eventList.item(EventIndex).text()
            print(f'| - runScript() [info] found event {self.Event} at {EventIndex}')
            for event in self.eventMaps:
                if search(event, self.Event):
                    print(f'| - runScript() [info] running event {self.Event}')
                    if len(paramLinkedToIndex[f'{EventIndex}']) == 2:
                        self.eventMaps[event](paramLinkedToIndex[f'{EventIndex}'][0],\
                                              paramLinkedToIndex[f'{EventIndex}'][1])
                    elif len(paramLinkedToIndex[f'{EventIndex}']) == 3:
                        self.eventMaps[event](paramLinkedToIndex[f'{EventIndex}'][0],\
                                              paramLinkedToIndex[f'{EventIndex}'][1],\
                                              paramLinkedToIndex[f'{EventIndex}'][2])
                else:
                    pass
                    #print(f'| - runScript() [error] failed to run event {self.Event}\n                        This may be due to it not being in the eventMap')

    def deleteAtCurrentIndex(self):
        try:
            print(f'| - deleteAtCurrentIndex() [info] removed item {self.lastItem}')
            self.index = self.eventList.indexFromItem(self.lastItem).row()
            self.eventList.takeItem(self.index)
        except Exception as e:
            print(f'| - deleteAtCurrentIndex() [info] no items selected or other reason: {e}')

    def editParamsAtCurrentIndex(self):
        try:
            self.index = self.eventList.indexFromItem(self.lastItem)
            self.itemAtCurrentEvent = self.eventList.itemFromIndex(self.index).text()
            for event in self.eventMaps:
                if search(event, self.itemAtCurrentEvent):
                    if len(paramLinkedToIndex[f'{self.index.row()}']) == 2:
                        self.paramMenu[f'{event}'](self.index.row(), paramLinkedToIndex[f'{self.index.row()}'][0], \
                                                                     paramLinkedToIndex[f'{self.index.row()}'][1])
                    if len(paramLinkedToIndex[f'{self.index.row()}']) == 2:
                        self.paramMenu[f'{event}'](self.index.row(), paramLinkedToIndex[f'{self.index.row()}'][0], \
                                                                     paramLinkedToIndex[f'{self.index.row()}'][1], \
                                                                     paramLinkedToIndex[f'{self.index.row()}'][2])
                else:
                    pass
        except Exception as e:
            print(f'| - deleteAtCurrentIndex() [info] no items selected or other reason: {e}')


class App(QMainWindow):
    def __init__(self):
        super(App, self).__init__()
        
        loadUi('ui/malmaker.ui', self)

        self.setWindowTitle('MalMaker for Windows - New Workspace')
        self.Icon = QIcon('assets/favicon.png')
        self.setWindowIcon(self.Icon)

        self.WelcomeWindowUI = WelcomeWindow()
        self.ScriptWindowUI = ScriptWindow()

        self.WelcomeWindow = self.workspace.addSubWindow(self.WelcomeWindowUI)
        self.ScriptWindow = self.workspace.addSubWindow(self.ScriptWindowUI)

        self.WelcomeWindow.show()
        self.ScriptWindow.show()

        print(self.workspace.subWindowList())

    def run():
        if __name__ == '__main__': 
            app = QApplication(sys.argv)
            ui = App()
            ui.show()
            app.exec_()


App.run()
