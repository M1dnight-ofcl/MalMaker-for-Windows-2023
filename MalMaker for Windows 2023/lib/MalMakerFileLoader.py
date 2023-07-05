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

class 