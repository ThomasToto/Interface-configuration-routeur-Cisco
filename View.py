# -*- coding: utf-8 -*-
"""
Created on Tue Apr 02 14:50:31 2021

@author: Thomas
"""

#=========== IMPORTATION ===========#

import sys, csv, shutil
from PyQt5.QtWidgets import (QLineEdit, QTableWidget, QInputDialog, QPushButton, QVBoxLayout, QHBoxLayout,
                             QApplication,qApp, QRadioButton, QMenuBar, QFileDialog, QFormLayout, QMainWindow, qApp, QGridLayout, QAction, QWidget,QLabel,QRadioButton)
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore

from Controller import Controller
from Model import Model

#===================================#




#============== VIEW ===============#

class View(QWidget):
    
   def __init__(self, ctrl, parent = None):
       
       # MVC
       self.myCtrl = ctrl
       
       
       # Héritage - Appel de la classe mère
       super(View, self).__init__(parent)
       
       # Initialisation variable globale
       global nomFichier      
       
       # Création layout
       self.layout = QFormLayout()
       
       # Menu bar
       self.menu = QMenuBar()
       self.menuFichier = self.menu.addMenu("Fichier") 
       self.layout.addRow(self.menu)

      
       # Création sous menu Ouvrir
       ouvrirMenu = QAction(QIcon('open.svg'),'Ouvrir', self)
       ouvrirMenu.setShortcut('Ctrl+O')
       ouvrirMenu.triggered.connect(lambda: self.openDb(self.myCtrl))
       self.menuFichier.addAction(ouvrirMenu)

       # Création sous menu Enregistrer
       enregistrerMenu = QAction(QIcon('save.svg'),'Enregistrer sous', self)
       enregistrerMenu.setShortcut('Ctrl+S')
       enregistrerMenu.triggered.connect(self.saveDb)
       self.menuFichier.addAction(enregistrerMenu)

       # Action sous menu Quitter
       quitterMenu = QAction(QIcon('exit.svg'),'Quitter', self)
       quitterMenu.setShortcut('Ctrl+Q')
       quitterMenu.triggered.connect(app.quit)
       quitterMenu.triggered.connect(self.close)
       self.menuFichier.addAction(quitterMenu)
       
       
       # Ajout des checkbox
       with open(nomFichier,'r') as csvfile:
           reader = csv.reader(csvfile, delimiter=',')
           
           for row in reader:
               try:
                   global compteur
                   if(len(row[0]) != 0) :
                       locals()['self.checkboxRouteur%d' % compteur] = QRadioButton(row[0])
                       self.layout.addWidget(locals()['self.checkboxRouteur%d' % compteur])                       
                   compteur += 1
               except IndexError:
                   pass
       
       
       # Création des boutons        
       self.buttonAdd = QPushButton("Ajouter un routeur")
       self.buttonSelect = QPushButton("Voir le routeur")
       self.buttonDelete = QPushButton("Supprimer le routeur")
       self.buttonEdit = QPushButton("Modifier le routeur")

       # Ajout des widgets au layout et mise en place du layout    
       self.layout.addRow(self.buttonSelect,self.buttonEdit)
       self.layout.addRow(self.buttonAdd,self.buttonDelete)
       self.setLayout(self.layout)
       

       # Filtre afin de désactiver les boutons si aucun routeur crée 
       if not self.findChildren(QRadioButton):
           self.buttonSelect.setEnabled(False)
           self.buttonDelete.setEnabled(False)
           self.buttonEdit.setEnabled(False)

       
       
       # Gestion des events
       self.buttonSelect.clicked.connect(lambda: self.btn_clickSelectRouteur(self.myCtrl))
       self.buttonAdd.clicked.connect(lambda: self.btn_clickAddRouteur(self.myCtrl))
       self.buttonDelete.clicked.connect(lambda: self.btn_clickDeleteRouteur(self.myCtrl))
       self.buttonEdit.clicked.connect(lambda: self.btn_clickEditRouteur(self.myCtrl))
       
       
       
       self.setWindowTitle("Accueil")
       self.show()
       
       

#=========== ROUTEUR ===========#

   def vueAjouterRouteur(self, myCtrl, parent = None):
       
       # Héritage - Appel de la classe mère
       super(View, self).__init__(parent)
       
       # Création du layout 
       self.layout = QFormLayout()

       # Mise en place des widgets
       self.text1 = QLabel()
       self.text1.setText("Nom : ")
       self.le1 = QLineEdit()
       self.layout.addRow(self.text1,self.le1)
      
       self.text2 = QLabel()
       self.text2.setText("Adresse IP : ")
       self.le2 = QLineEdit()
       self.layout.addRow(self.text2,self.le2)
      
       self.text3 = QLabel()
       self.text3.setText("Masque de sous réseaux : ")
       self.le3 = QLineEdit()
       self.layout.addRow(self.text3,self.le3)
            
       self.buttonSave = QPushButton("Ajouter le routeur")
       self.buttonCancel = QPushButton("Annuler")
       
       
       # Gestion des events
       self.buttonSave.clicked.connect(lambda: self.btn_clickAddSaveRouteur(myCtrl))
       self.buttonCancel.clicked.connect(lambda: self.btn_clickCancelRouteur(myCtrl))
       self.layout.addRow(self.buttonSave, self.buttonCancel)
       
       
       self.setLayout(self.layout)
       self.setWindowTitle("Ajouter un routeur")
       self.show()
       
   def vueConfigRouteur(self,myCtrl, nomRouteur, adresseIP,masque, parent = None):
       
       # Héritage - appel de la classe mère
       super(View, self).__init__(parent)		
       
       # Création du layout
       self.layout = QFormLayout() 

       # Mise en place des widgets            
       self.text1 = QLabel()
       self.text1.setText("Nom : ")
       self.le1 = QLineEdit()
       self.le1.setText(nomRouteur)
       self.le1.setEnabled(False)
       self.layout.addRow(self.text1,self.le1)
      
       self.text2 = QLabel()
       self.text2.setText("Adresse IP : ")
       self.le2 = QLineEdit()
       self.le2.setText(adresseIP)
       self.layout.addRow(self.text2,self.le2)
       
       self.text3 = QLabel()
       self.text3.setText("Masque de sous réseaux : ")
       self.le3 = QLineEdit()
       self.le3.setText(masque)
       self.layout.addRow(self.text3,self.le3)
      
       self.buttonSaveRouteur = QPushButton("Enregistrer")
       self.buttonCancelRouteur = QPushButton("Annuler")
       
       self.layout.addRow(self.buttonSaveRouteur, self.buttonCancelRouteur)
       
       # Gestion des events
       self.buttonSaveRouteur.clicked.connect(lambda: self.btn_clickEditSaveRouteur(myCtrl,self.le1.text(),self.le2.text(),self.le3.text()))
       self.buttonCancelRouteur.clicked.connect(lambda: self.btn_clickCancelRouteur(myCtrl))
       
             
       self.setLayout(self.layout)
       self.setWindowTitle("Configuration du routeur : " + nomRouteur)
       self.show()
       
   def btn_clickEditRouteur(self,myCtrl): 
       global nomFichier
       self.close()
       for items in self.findChildren(QRadioButton):
           if items.isChecked():
               reponse = self.myCtrl.editRouteur(nomFichier,items)


       if(reponse[0] == True):
           self.vueConfigRouteur(myCtrl,reponse[1],reponse[2],reponse[3])
                                             
       
       
   def btn_clickDeleteRouteur(self,myCtrl):   
       global nomFichier
       
       for items in self.findChildren(QRadioButton):
               myCtrl.deleteRouteur(nomFichier,items)                  
       self.close()
       self.__init__(myCtrl)


   def btn_clickSelectRouteur(self,myCtrl):
       self.close()
       for items in self.findChildren(QRadioButton):
           if items.isChecked():
               nomRouteur = items.text()
       self.accueilInterface(myCtrl,nomRouteur)
       


   def btn_clickAddRouteur(self,myCtrl):
       self.close()
       self.vueAjouterRouteur(myCtrl)


   def btn_clickCancelRouteur(self,myCtrl):   
       self.close()
       self.__init__(myCtrl)


   def btn_clickAddSaveRouteur(self,myCtrl):
       global nomFichier
       
       textLe1 = self.le1.text()
       textLe2 = self.le2.text()
       textLe3 = self.le3.text()
       
       myCtrl.addSaveRouteur(nomFichier,textLe1,textLe2,textLe3)
              
       self.close()    
       self.__init__(myCtrl)

 
   def btn_clickEditSaveRouteur(self,myCtrl, nomRouteur,adresseIP,masque):
       global nomFichier
       
       myCtrl.editSaveRouteur(nomFichier,nomRouteur,adresseIP,masque)
       
       
       self.close()
       self.__init__(myCtrl)




#=========== INTERFACE ===========#

   def accueilInterface(self,myCtrl, nomRouteur,parent = None):
       
       # Initialisation variable globale
       global nomFichier
       
       # Héritage - appel à la classe mère
       super(View, self).__init__(parent)
       
       # Mise en place du layout
       self.layout = QFormLayout()
       
       # Menu Bar
       self.menu = QMenuBar()
       self.menuFichier = self.menu.addMenu("Fichier") 
       self.layout.addRow(self.menu)

      
       # Création sous menu Ouvrir
       ouvrirMenu = QAction(QIcon('open.svg'),'Ouvrir', self)
       ouvrirMenu.setShortcut('Ctrl+O')
       ouvrirMenu.triggered.connect(lambda: self.openDb(myCtrl))
       self.menuFichier.addAction(ouvrirMenu)

       # Création sous menu Enregistrer
       enregistrerMenu = QAction(QIcon('save.svg'),'Enregistrer sous', self)
       enregistrerMenu.setShortcut('Ctrl+S')
       enregistrerMenu.triggered.connect(self.saveDb)
       self.menuFichier.addAction(enregistrerMenu)

       # Action sous menu Quitter
       quitterMenu = QAction(QIcon('exit.svg'),'Quitter', self)
       quitterMenu.setShortcut('Ctrl+Q')
       quitterMenu.triggered.connect(app.quit)
       quitterMenu.triggered.connect(self.close)
       self.menuFichier.addAction(quitterMenu)
       
       
       # Ajout des checkbox 
       with open(nomFichier,'r') as f:
           lignes = f.readlines()
           
           for ligneCourante in lignes:
               if(ligneCourante.split(',')[0] == nomRouteur):
                   try:
                       global compteur
                       for i in range(3,len(ligneCourante),4):
                           if(len(ligneCourante.split(",")[i].strip()) != 0) :
                               locals()['self.checkboxInterface%d' % compteur] = QRadioButton(ligneCourante.split(",")[i])
                               self.layout.addWidget(locals()['self.checkboxInterface%d' % compteur])                       
                       compteur += 1 
                   except IndexError:
                       pass
       
       
       # Mise en place de la table de routage
       self.tableRoutage = QTableWidget(5,3)
       self.tableRoutage.setHorizontalHeaderLabels(['Destination réseau', 'Masque réseau', 'Adresse passerelle'])
       
       # Création des boutons
       self.buttonAdd = QPushButton("Ajouter une interface")
       self.buttonSelect = QPushButton("Voir l'interface")
       self.buttonDelete = QPushButton("Supprimer l'interface")
       self.buttonBackHome = QPushButton("Revenir à l'accueil")

       # Ajout des widgets au layout
       self.layout.addRow(self.tableRoutage)    
       self.layout.addRow(self.buttonSelect)
       self.layout.addRow(self.buttonAdd,self.buttonDelete)
       self.layout.addRow(self.buttonBackHome)
       
       
       self.setLayout(self.layout)
       
       # Filtre afin de désactiver les boutons si aucun routeur crée 
       if not self.findChildren(QRadioButton):
           self.buttonSelect.setEnabled(False)
           self.buttonDelete.setEnabled(False)

       # Gestion des events
       self.buttonSelect.clicked.connect(lambda: self.btn_clickSelectInterface(myCtrl,nomRouteur))
       self.buttonAdd.clicked.connect(lambda: self.btn_clickAddInterface(myCtrl,nomRouteur))
       self.buttonDelete.clicked.connect(lambda: self.btn_clickDeleteInterface(myCtrl,nomRouteur))
       self.buttonBackHome.clicked.connect(lambda: self.btn_clickBackHome(myCtrl))

       
       self.setWindowTitle("Choix interface du routeur : " + nomRouteur)
       self.show()
       
       

   def vueAjouterInterface(self,myCtrl,nomRouteur, parent = None):
       
       # Héritage - appel à la classe mère
       super(View, self).__init__(parent)		
       
       # Mise en place du layout
       self.layout = QFormLayout()

       # Mise en place des widgets 
       self.text1 = QLabel()
       self.text1.setText("Nom : ")
       self.le1 = QLineEdit()
       self.layout.addRow(self.text1,self.le1)
      
       self.text2 = QLabel()
       self.text2.setText("Adresse IP : ")
       self.le2 = QLineEdit()
       self.layout.addRow(self.text2,self.le2)
      
       self.text3 = QLabel()
       self.text3.setText("Masque de sous réseaux : ")
       self.le3 = QLineEdit()
       self.layout.addRow(self.text3,self.le3)
      
       self.text4 = QLabel()
       self.text4.setText("Passerelle par défaut : ")
       self.le4 = QLineEdit()
       self.layout.addRow(self.text4,self.le4)
       
       self.buttonSave = QPushButton("Ajouter l'interface")
       self.buttonCancel = QPushButton("Annuler")
       
       self.layout.addRow(self.buttonSave, self.buttonCancel)
       self.setLayout(self.layout)
       
       # Gestion des events
       self.buttonSave.clicked.connect(lambda: self.btn_clickAddSaveInterface(myCtrl,nomRouteur))
       self.buttonCancel.clicked.connect(lambda: self.btn_clickCancelInterface(myCtrl,nomRouteur))
       
       
       self.setWindowTitle("Ajouter une interface")
       self.show()
       
   def vueConfigInterface(self, myCtrl,nomRouteur, nomInterface, adresseIP, masque, passerelleDefaut, parent = None):
       
       # Héritage - appel à la classe mère
       super(View, self).__init__(parent)		
       
       # Création du layout
       self.layout = QFormLayout()  

       # Mise en place des widgets
       self.text1 = QLabel()
       self.text1.setText("Nom : ")
       self.le1 = QLineEdit()
       self.le1.setText(nomInterface)
       self.le1.setEnabled(False)
       self.layout.addRow(self.text1,self.le1)
      
       self.text2 = QLabel()
       self.text2.setText("Adresse IP : ")
       self.le2 = QLineEdit()
       self.le2.setText(adresseIP)
       self.layout.addRow(self.text2,self.le2)
       
       self.text3 = QLabel()
       self.text3.setText("Masque de sous réseaux : ")
       self.le3 = QLineEdit()
       self.le3.setText(masque)
       self.layout.addRow(self.text3,self.le3)
      
       self.text4 = QLabel()
       self.text4.setText("Passerelle par défaut : ")
       self.le4 = QLineEdit()
       self.le4.setText(passerelleDefaut)
       self.layout.addRow(self.text4,self.le4)
      
       self.buttonSaveInterface = QPushButton("Enregistrer")
       self.buttonCancelInterface = QPushButton("Annuler")
       
       self.layout.addRow(self.buttonSaveInterface, self.buttonCancelInterface)
       
       # Gestion des events
       self.buttonSaveInterface.clicked.connect(lambda: self.btn_clickEditSaveInterface(myCtrl,nomRouteur,self.le1.text(),self.le2.text(),self.le3.text(),self.le4.text()))
       self.buttonCancelInterface.clicked.connect(lambda: self.btn_clickCancelInterface(myCtrl,nomRouteur))

       
       self.setLayout(self.layout)
       self.setWindowTitle("Configuration de l'interface : " + nomInterface)
       self.show()
      

       
   def btn_clickBackHome(self,myCtrl):
       self.close()
       self.__init__(myCtrl)

   def btn_clickAddInterface(self,myCtrl,nomRouteur):
       self.close()
       self.vueAjouterInterface(myCtrl,nomRouteur)

   def btn_clickDeleteInterface(self,myCtrl,nomRouteur):   
       global nomFichier
       
       for items in self.findChildren(QRadioButton):
           myCtrl.deleteInterface(nomFichier,nomRouteur,items)
       self.close()
       self.accueilInterface(myCtrl, nomRouteur)


       
   def btn_clickSelectInterface(self,myCtrl,nomRouteur):
       global nomFichier
       self.close()
       indicateur = False
       for items in self.findChildren(QRadioButton):
           if items.isChecked():
               indicateur = True
               reponse = myCtrl.selectInterface(nomFichier,nomRouteur,items)
               
       if(reponse[0] == True):
           self.vueConfigInterface(myCtrl,nomRouteur,reponse[1],reponse[2],reponse[3],reponse[4])

                    
       # Si aucun bouton radio est check mais qu'on appuie quand meme sur "Sélectionner"               
       if indicateur == False:
           self.accueilInterface(myCtrl,nomRouteur) 
                   
               
   def btn_clickAddSaveInterface(self,myCtrl,nomRouteur):
       global nomFichier
       
       textLe1 = self.le1.text()
       textLe2 = self.le2.text()
       textLe3 = self.le3.text()
       textLe4 = self.le4.text()
       
       myCtrl.addSaveInterface(nomFichier,nomRouteur,textLe1,textLe2,textLe3,textLe4)
       
       self.close()    
       self.accueilInterface(myCtrl,nomRouteur)

 
   def btn_clickEditSaveInterface(self,myCtrl, nomRouteur,nomInterface,adresseIP,masque,passerelleDefaut):
       global nomFichier
       
       myCtrl.editSaveInterface(nomFichier,nomRouteur,nomInterface,adresseIP,masque,passerelleDefaut)
       
       
       self.close()
       self.accueilInterface(myCtrl,nomRouteur)

   def btn_clickCancelInterface(self,myCtrl,nomRouteur):   
       self.close()
       self.accueilInterface(myCtrl,nomRouteur)
     
        
     
   def saveDb(self):
       try:
           savName = QFileDialog.getSaveFileName(self, 'Sauvegarder fichier','c:\\',"Data files (*.csv)")
           global nomFichier
           shutil.copyfile(nomFichier, savName[0])
       except FileNotFoundError:
           pass
           
           
       
   def openDb(self,myCtrl):
       global nomFichier
       try:
           fname = QFileDialog.getOpenFileName(self, 'Ouvrir fichier','G:/EPISEN/ITS 1/S2/IHM/Projet/Test solo/',"Data files (*.csv)")          
           nomFichier = fname[0]
           self.close()
           self.__init__(myCtrl)
       except FileNotFoundError:
           nomFichier = 'database.csv'
           self.__init__(myCtrl)
           
           
        
# Permet d'éxecuter le script ci-dessous en premier
if __name__ == '__main__':
   app = QApplication(sys.argv)
   global compteur 
   compteur = 1
   global nomFichier
   nomFichier = 'database.csv'
   creationFichier = open(nomFichier, 'w')
   model = Model()
   ctrl = Controller(model)
   view = View(ctrl)
   sys.exit(app.exec_())