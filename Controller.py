# -*- coding: utf-8 -*-
"""
Created on Tue Apr 02 14:51:55 2021

@author: Thomas
"""


#=========== IMPORTATION ===========#


#===================================#



#============== CONTROLLER ===============#

class Controller:
    def __init__(self, model):
        self.myModel = model
        
    def deleteRouteur(self,nomFichier,items):
        self.myModel.deleteRouteur(nomFichier,items)
        
    def addSaveRouteur(self,nomFichier, text1,text2,text3):
        self.myModel.addSaveRouteur(nomFichier,text1,text2,text3)
        
        
    def editSaveRouteur(self,nomFichier,nomRouteur,adresseIP,masque):
        self.myModel.editSaveRouteur(nomFichier,nomRouteur,adresseIP,masque)
        
        
    def deleteInterface(self,nomFichier,nomRouteur,items):
        self.myModel.deleteInterface(nomFichier,nomRouteur,items)
        
        
    def addSaveInterface(self,nomFichier,nomRouteur,text1,text2,text3,text4):
        self.myModel.addSaveInterface(nomFichier,nomRouteur,text1,text2,text3,text4)

    def editSaveInterface(self,nomFichier,nomRouteur,nomInterface,masque,adresseIP,passerelleDefaut) :
        self.myModel.editSaveInterface(nomFichier,nomRouteur,nomInterface,masque,adresseIP,passerelleDefaut)

    def editRouteur(self,nomFichier,items):
        return self.myModel.editRouteur(nomFichier,items)

    def selectInterface(self,nomFichier,nomRouteur,items):
        return self.myModel.selectInterface(nomFichier,nomRouteur,items)
    

        