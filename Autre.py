# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 14:50:31 2021

@author: Thomas
"""

# Importation
import sys
from PyQt5.QtWidgets import (QLineEdit, QInputDialog, QPushButton, QVBoxLayout, QHBoxLayout,
                             QApplication, QMenuBar, QFileDialog, QFormLayout, QMainWindow, qApp, QGridLayout, QAction, QWidget,QLabel,QRadioButton)
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore

from Controller import Controller
from Model import Model


class inputdialog (QWidget):
   def __init__(self, parent = None):
      super(inputdialog, self).__init__(parent)
		
      layout = QFormLayout()

      self.text1 = QLabel()
      self.text1.setText("Nom : ")
      self.le1 = QLineEdit()
      layout.addRow(self.text1,self.le1)
      
      self.text2 = QLabel()
      self.text2.setText("Adresse IP : ")
      self.le2 = QLineEdit()
      layout.addRow(self.text2,self.le2)
      
      self.text3 = QLabel()
      self.text3.setText("Masque de sous réseaux : ")
      self.le3 = QLineEdit()
      layout.addRow(self.text3,self.le3)
      
      self.text4 = QLabel()
      self.text4.setText("Passerelle par défaut : ")
      self.le4 = QLineEdit()
      layout.addRow(self.text4,self.le4)
      
      self.setLayout(layout)
      self.setWindowTitle("Ajouter un routeur")

      self.show()

class WindowIntro (QWidget):

    # Constructeur
    def __init__(self, ctrl):
        super().__init__()
        self.windowM = None
        self.myCtrl = ctrl
        
        # Bouton
        self.b = QPushButton("Commencer")
        
        # Texte
        self.text = QLabel()
        self.text.setText("Interface configuration routeur")

        
        # Paramètres fenêtre
        self.setGeometry(50, 50, 1000, 700)
        self.setWindowTitle('Accueil')
        
        
        self.init_ui()

        # Affiche la fenêtre 
        self.show()


    def init_ui(self):

        # Event
        self.b.clicked.connect(self.btn_click)


        # Affichage
        h_box = QHBoxLayout()
        h_box.addWidget(self.text)
        h_box.setAlignment(QtCore.Qt.AlignCenter)
        
        h_box2 = QHBoxLayout()
        h_box2.addWidget(self.b)
        h_box2.setAlignment(QtCore.Qt.AlignCenter)
        
        
        v_box = QVBoxLayout()
        v_box.setAlignment(QtCore.Qt.AlignCenter)

        v_box.addLayout(h_box)
        v_box.addLayout(h_box2)


        self.setLayout(v_box)



    # Event si commencement configuration
    def btn_click(self):
        self.myCtrl.newWindow(self.windowM,WindowMain,a_window)
        
    


class WindowMain (QWidget):

    def __init__(self):
        super().__init__()
        self.myCtrl = ctrl
        
        layout = QGridLayout()
        self.setLayout(layout)
        

        
        # Création menu général
        menubar = QMenuBar()
        layout.addWidget(menubar, 0, 0)
        menu = menubar.addMenu("Fichier")
        
        # Création sous menu Ouvrir
        ouvrirMenu = QAction(QIcon('open.svg'),'Ouvrir', self)
        ouvrirMenu.setShortcut('Ctrl+O')
        ouvrirMenu.triggered.connect(self.open)
        menu.addAction(ouvrirMenu)

        # Création sous menu Enregistrer
        enregistrerMenu = QAction(QIcon('save.svg'),'Enregistrer', self)
        enregistrerMenu.setShortcut('Ctrl+S')
        menu.addAction(enregistrerMenu)

        # Action sous menu Quitter
        quitterMenu = QAction(QIcon('exit.svg'),'Quitter', self)
        quitterMenu.setShortcut('Ctrl+Q')
        quitterMenu.triggered.connect(app.quit)
        quitterMenu.triggered.connect(self.close)
        menu.addAction(quitterMenu)
        
        # interface principale
        self.routeur = QLabel()
        self.routeur.setText("Liste des routeurs disponibles : ")
        layout.addWidget(self.routeur)
        self.btnAdd = QPushButton("Ajouter un routeur")
        layout.addWidget(self.btnAdd)
        
        # Event
        self.btnAdd.clicked.connect(lambda: self.btnAdd_click(layout))
        

        self.setGeometry(50, 50, 1000, 700)
        self.setWindowTitle('Configuration')
        self.show()
        
        
    def btnAdd_click(self,layout):
        inputdialog()

        
        
        
    def open(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file','c:\\',"Image files (*.jpg *.gif)")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    model = Model()
    ctrl = Controller(model)
    a_window= WindowIntro(ctrl)
    sys.exit(app.exec_())

