# -*- coding: utf-8 -*-
"""
Created on Thu Mar 11 21:57:38 2021

@author: Thomas
"""

class Controller:
    def __init__(self, model):
        self.myModel = model
        
    def newWindow(self,windowM, WindowMain,WindowIntro):
        WindowIntro.close()
        WindowIntro.windowM = WindowMain()

    def addButton(self, layout,lineName):
        layout.addWidget(lineName)

        