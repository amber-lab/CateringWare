# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
Created on Thu Mar 26 21:53:30 2020

@author: L.A.B
"""
import os
import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"include_files" : ['C:/Users/L.A.B/Desktop/CateringCalculator/CateringDB.db',
                                        'C:/Users/L.A.B/Desktop/CateringCalculator/img'],
                      'build_exe' : '.\\CateringWare'}

# GUI applications require a different base on Windows (the default is for a
# console application).
os.environ['TCL_LIBRARY'] = "C:\\Users\\L.A.B\\Anaconda3_32\\tcl\\tcl8.6"
os.environ['TK_LIBRARY'] = "C:\\Users\\L.A.B\\Anaconda3_32\\tcl\\tk8.6"


# base='Console'
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "CateringWare",
        version = "0.1",
        description = "CateringWare",
        options = {"build_exe": build_exe_options},
        executables = [Executable("CateringWare.py", base=base, targetName = 'CateringWare.exe', icon = 'icon.ico')])

