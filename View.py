# -*- coding:utf-8 -*-
"""
Created on Tue Apr 02 14:50:31 2021

@author: Thomas
"""

#=========== IMPORTATION ===========#

import sys, csv, shutil
from PyQt5.QtWidgets import (QLineEdit, QPushButton,
                             QApplication, QRadioButton,QTextEdit, QMenuBar, QFileDialog, QFormLayout, QAction, QWidget,QLabel)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize

from Controller import Controller
from Model import Model

#===================================#




#============== VIEW ===============#

class View(QWidget):
    '''
        Paramètres : 
            - QWidget est la classe de base de tous les objets d'interface utilisateur.  
            
        But : Fonction qui met en place la vue d'accueil.
    '''    
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
       ouvrirMenu = QAction(QIcon('Logo\open.svg'),'Ouvrir', self)
       ouvrirMenu.setShortcut('Ctrl+O')
       ouvrirMenu.triggered.connect(lambda: self.openDb(self.myCtrl))
       self.menuFichier.addAction(ouvrirMenu)

       # Création sous menu Enregistrer
       enregistrerMenu = QAction(QIcon('Logo\save.svg'),'Enregistrer sous', self)
       enregistrerMenu.setShortcut('Ctrl+S')
       enregistrerMenu.triggered.connect(self.saveDb)
       self.menuFichier.addAction(enregistrerMenu)

       # Action sous menu Quitter
       quitterMenu = QAction(QIcon('Logo\exit.svg'),'Quitter', self)
       quitterMenu.setShortcut('Ctrl+Q')
       quitterMenu.triggered.connect(app.quit)
       quitterMenu.triggered.connect(self.close)
       self.menuFichier.addAction(quitterMenu)
       
       # Texte liste routeur
       self.textList = QLabel("Listes des routeurs :")
       self.layout.addRow(self.textList)
       
       # Ajout des checkbox
       with open(nomFichier,'r') as csvfile:
           reader = csv.reader(csvfile, delimiter=',')
           
           for row in reader:
               try:
                   global compteur
                   if(len(row[0]) != 0) :
                       locals()['self.checkboxRouteur%d' % compteur] = QRadioButton(row[0])
                       locals()['self.checkboxRouteur%d' % compteur].setIcon(QIcon('Logo\iconRouteur.svg'))
                       self.layout.addWidget(locals()['self.checkboxRouteur%d' % compteur])  
                       
                   compteur += 1
               except IndexError:
                   pass
       
       
       # Création des boutons        
       self.buttonAdd = QPushButton("Ajouter un routeur")
       self.buttonAdd.setIcon(QIcon('Logo\plus.svg'))
       self.buttonSelect = QPushButton("Voir le routeur")
       self.buttonSelect.setIcon(QIcon('Logo\select.svg'))
       self.buttonDelete = QPushButton("Supprimer le routeur")
       self.buttonDelete.setIcon(QIcon('Logo\delete.svg'))
       self.buttonEdit = QPushButton("Modifier le routeur")
       self.buttonEdit.setIcon(QIcon('Logo\edit.svg'))

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
       self.setGeometry(500, 200, 500, 200)
       
       

#=========== ROUTEUR ===========#

    def vueAjouterRouteur(self, myCtrl, parent = None):
        '''
        Paramètres : 
            - myCtrl (Controller) : instance de la classe Controller    
            
        But : Fonction qui met en place la vue d'ajout d'un routeur.
        '''  
        
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
        self.text3.setText(u"Masque de sous réseaux : ")
        self.le3 = QLineEdit()
        self.layout.addRow(self.text3,self.le3)
            
        self.buttonSave = QPushButton("Ajouter le routeur")
        self.buttonSave.setIcon(QIcon('Logo\plus.svg'))
        self.buttonCancel = QPushButton("Annuler")
        self.buttonCancel.setIcon(QIcon('Logo\exit.svg'))
       
       
        # Gestion des events
        self.buttonSave.clicked.connect(lambda: self.btn_clickAddSaveRouteur(myCtrl))
        self.buttonCancel.clicked.connect(lambda: self.btn_clickCancelRouteur(myCtrl))
        self.layout.addRow(self.buttonSave, self.buttonCancel)
       
       
        self.setLayout(self.layout)
        self.setWindowTitle("Ajouter un routeur")
        self.show()
       
    def vueConfigRouteur(self,myCtrl, nomRouteur, adresseIP,masque, parent = None):
        '''
        Paramètres : 
            - myCtrl (Controller) : instance de la classe Controller    
            - nomRouteur (String) : nom du routeur possédant l'interface
            - adresseIP (String) : adresse IP du routeur
            - masque (String) : masque du routeur
            
        But : Fonction qui met en place la vue de configuration d'un routeur.
        '''   
        
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
        self.buttonSaveRouteur.setIcon(QIcon('Logo\save.svg'))
        self.buttonCancelRouteur = QPushButton("Annuler")
        self.buttonCancelRouteur.setIcon(QIcon('Logo\exit.svg'))       
        self.layout.addRow(self.buttonSaveRouteur, self.buttonCancelRouteur)
       
        # Gestion des events
        self.buttonSaveRouteur.clicked.connect(lambda: self.btn_clickEditSaveRouteur(myCtrl,self.le1.text(),self.le2.text(),self.le3.text()))
        self.buttonCancelRouteur.clicked.connect(lambda: self.btn_clickCancelRouteur(myCtrl))
       
             
        self.setLayout(self.layout)
        self.setWindowTitle("Configuration du routeur : " + nomRouteur)
        self.show()
       
    def btn_clickEditRouteur(self,myCtrl): 
        '''
        Paramètres : 
            - myCtrl (Controller) : instance de la classe Controller
            
        But : Fonction appelant la fonction deleteRouteur permettant de supprimer un routeur.
        
        Fonctionnement : Fermer la fenêtre courante. Trouver quel routeur est choisi. Appeller la fonction
                         editRouteur puis appeller la vue gerant la configuration des routeurs avec les 
                         informations du routeur choisi.
        '''          
        global nomFichier
        self.close()
        for items in self.findChildren(QRadioButton):
            if items.isChecked():
                reponse = self.myCtrl.editRouteur(nomFichier,items)


        if(reponse[0] == True):
            self.vueConfigRouteur(myCtrl,reponse[1],reponse[2],reponse[3])
                                             
       
       
    def btn_clickDeleteRouteur(self,myCtrl):  
        '''
        Paramètres : 
            - myCtrl (Controller) : instance de la classe Controller
            
        But : Fonction appelant la fonction deleteRouteur permettant de supprimer un routeur.
        
        Fonctionnement : Trouver quel routeur est choisi. Fermer la fenêtre courante puis lancer la vue de l'accueil 
                         des interfaces du routeur.
        '''   
        global nomFichier
       
        for items in self.findChildren(QRadioButton):
                myCtrl.deleteRouteur(nomFichier,items)                  
        self.close()
        self.__init__(myCtrl)


    def btn_clickSelectRouteur(self,myCtrl):
        '''
        Paramètres : 
            - myCtrl (Controller) : instance de la classe Controller
            
        But : Fonction appelant la vue de l'accueil des interfaces.
        
        Fonctionnement : Fermer la fenêtre courante. Trouver quel routeur est choisi puis lancer la vue de l'accueil 
                         des interfaces du routeur.
        '''         
        self.close()
        for items in self.findChildren(QRadioButton):
            if items.isChecked():
                nomRouteur = items.text()
        self.accueilInterface(myCtrl,nomRouteur)
       


    def btn_clickAddRouteur(self,myCtrl):
        '''
        Paramètres : 
            - myCtrl (Controller) : instance de la classe Controller
            
        But : Fonction appelant la vue chargée d'ajouter un routeur.
        
        Fonctionnement : Fermer la fenêtre courante puis lancer la vue chargée d'ajouter un routeur.
        '''          
        self.close()
        self.vueAjouterRouteur(myCtrl)


    def btn_clickCancelRouteur(self,myCtrl):  
        '''
        Paramètres : 
            - myCtrl (Controller) : instance de la classe Controller
            
        But : Fonction permettant d'annuler l'enregistrement, la modification et l'ajout d'une interface.
        
        Fonctionnement : Fermer la fenêtre courante puis lancer la vue de l'accueil des interfaces.
        '''    
        self.close()
        self.__init__(myCtrl)


    def btn_clickAddSaveRouteur(self,myCtrl):
        '''
        Paramètres :
            - myCtrl (Controller) : instance de la classe Controller            
            
        But : Effectuer la sauvegarde du nouveau routeur en question via l'appel de la fonction
              addSaveRouteur.
        
        Fonctionnement : Appeler la fonction addSaveRouteur. Puis fermer la 
              fenêtre courante et lancer la vue de l'accueil.
        '''   
        global nomFichier
       
        textLe1 = self.le1.text()
        textLe2 = self.le2.text()
        textLe3 = self.le3.text()
       
        myCtrl.addSaveRouteur(nomFichier,textLe1,textLe2,textLe3)
              
        self.close()    
        self.__init__(myCtrl)

 
    def btn_clickEditSaveRouteur(self,myCtrl, nomRouteur,adresseIP,masque):
        '''
        Paramètres :
            - myCtrl (Controller) : instance de la classe Controller            
            - nomRouteur (String) : nom du routeur
            - adresseIP (String) : adresse IP du routeur
            - masque (String) : masque du routeur

            
        But : Effectuer la sauvegarde des modifications du routeur en question via l'appel de la fonction
              editSaveRouteur.
        
        Fonctionnement : Appeler la fonction editSaveRouteur. Puis fermer la 
              fenêtre courante et lancer la vue de l'accueil.
        '''        
        global nomFichier
       
        myCtrl.editSaveRouteur(nomFichier,nomRouteur,adresseIP,masque)
       
       
        self.close()
        self.__init__(myCtrl)




#=========== INTERFACE ===========#

    def accueilInterface(self,myCtrl, nomRouteur,parent = None):
        '''
        Paramètres : 
            - myCtrl (Controller) : instance de la classe Controller    
            - nomRouteur (String) : nom du routeur possédant l'interface
            
        But : Fonction qui met en place la vue d'accueil.
        '''   
        
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
       
        # Texte liste interface
        self.textList = QLabel("Listes des interfaces :")
        self.layout.addRow(self.textList)
       
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
        self.tableRoutage = QTextEdit()
        route = myCtrl.sshShowRoute(nomFichier,nomRouteur)
        self.tableRoutage.setText("Table de routage :\n" +route)
        self.tableRoutage.setEnabled(False)
        
        # Création des boutons
        self.buttonDeleteRoute = QPushButton("Supprimer une route")
        self.buttonDeleteRoute.setIcon(QIcon('Logo\delete.svg'))   
        self.buttonAddRoute = QPushButton("Ajouter une route")
        self.buttonAddRoute.setIcon(QIcon('Logo\plus.svg'))
        self.buttonAdd = QPushButton("Ajouter une interface")
        self.buttonAdd.setIcon(QIcon('Logo\plus.svg'))
        self.buttonSelect = QPushButton("Voir l'interface")
        self.buttonSelect.setIcon(QIcon('Logo\select.svg'))
        self.buttonDelete = QPushButton("Supprimer l'interface")
        self.buttonDelete.setIcon(QIcon('Logo\delete.svg'))
        self.buttonBackHome = QPushButton("Revenir à l'accueil")
        self.buttonBackHome.setIcon(QIcon('Logo\home.svg'))

        # Ajout des widgets au layout
        self.layout.addRow(self.tableRoutage)
        self.layout.addRow(self.buttonAddRoute,self.buttonDeleteRoute) 
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
        self.buttonAddRoute.clicked.connect(lambda: self.btn_clickShowVueAddRoute(myCtrl,nomRouteur))
        self.buttonDeleteRoute.clicked.connect(lambda: self.btn_clickShowVueDeleteRoute(myCtrl,nomRouteur))
       
        self.setWindowTitle("Choix interface du routeur : " + nomRouteur)
        self.setGeometry(500, 200, 500, 400)
        self.show()
       
       

    def vueAjouterInterface(self,myCtrl,nomRouteur, parent = None):
        '''
        Paramètres : 
            - myCtrl (Controller) : instance de la classe Controller    
            - nomRouteur (String) : nom du routeur possédant l'interface
            
        But : Fonction qui met en place la vue permettant d'ajouter une interface.
        '''   
        
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
        self.buttonSave.setIcon(QIcon('Logo\plus.svg'))        
        self.buttonCancel = QPushButton("Annuler")
        self.buttonCancel.setIcon(QIcon('Logo\exit.svg'))
        
        self.layout.addRow(self.buttonSave, self.buttonCancel)
        self.setLayout(self.layout)
       
        # Gestion des events
        self.buttonSave.clicked.connect(lambda: self.btn_clickAddSaveInterface(myCtrl,nomRouteur))
        self.buttonCancel.clicked.connect(lambda: self.btn_clickCancelInterface(myCtrl,nomRouteur))
       
       
        self.setWindowTitle("Ajouter une interface")
        self.show()
       
    def vueConfigInterface(self, myCtrl,nomRouteur, nomInterface, adresseIP, masque, passerelleDefaut, parent = None):
        '''
        Paramètres : 
            - myCtrl (Controller) : instance de la classe Controller    
            - nomRouteur (String) : nom du routeur possédant l'interface
            - nomInterface (String) : nom de l'interface modifiée
            - adresseIP (String) : adresse IP de l'interface modifiée
            - masque (String) : masque de l'interface modifiée
            - passerelleDefaut (String) : passerelle par defaut de l'interface modifiée
            
        But : Fonction qui met en place la vue permettant de configurer une interface.
        '''      
        
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
        self.buttonSaveInterface.setIcon(QIcon('Logo\save.svg'))        
        self.buttonCancelInterface = QPushButton("Annuler")
        self.buttonCancelInterface.setIcon(QIcon('Logo\exit.svg')) 
        
 
        self.layout.addRow(self.buttonSaveInterface, self.buttonCancelInterface)
       
        # Gestion des events
        self.buttonSaveInterface.clicked.connect(lambda: self.btn_clickEditSaveInterface(myCtrl,nomRouteur,self.le1.text(),self.le2.text(),self.le3.text(),self.le4.text()))
        self.buttonCancelInterface.clicked.connect(lambda: self.btn_clickCancelInterface(myCtrl,nomRouteur))

       
        self.setLayout(self.layout)
        self.setWindowTitle("Configuration de l'interface : " + nomInterface)
        self.show()
      

    def btn_clickShowVueAddRoute(self,myCtrl,nomRouteur):
        '''
        Paramètres :
            - myCtrl (Controller) : instance de la classe Controller            
            - nomRouteur (String) : nom du routeur
            
        But : Afficher la vue permettant d'ajouter une route.
        
        Fonctionnement : Fermer la fenêtre courante puis lancer la vue chargée de l'ajout d'une route.
        ''' 
        self.close()
        self.vueAddRoute(myCtrl,nomRouteur)

    def btn_clickShowVueDeleteRoute(self,myCtrl,nomRouteur):
        '''
        Paramètres :
            - myCtrl (Controller) : instance de la classe Controller            
            - nomRouteur (String) : nom du routeur
            
        But : Afficher la vue permettant de supprimer une route.
        
        Fonctionnement : Fermer la fenêtre courante puis lancer la vue chargée de la suppression d'une route.
        ''' 
        self.close()
        self.vueDeleteRoute(myCtrl,nomRouteur)
       
    def btn_clickBackHome(self,myCtrl):
        '''
        Paramètres :
            - myCtrl (Controller) : instance de la classe Controller            
            
        But : Retourner à la page d'accueil
        
        Fonctionnement : Fermer la fenêtre courante puis lancer la vue de l'accueil.
        ''' 
        self.close()
        self.__init__(myCtrl)

    def btn_clickAddInterface(self,myCtrl,nomRouteur):
        '''
        Paramètres :
            - myCtrl (Controller) : instance de la classe Controller            
            - nomRouteur (String) : nom du routeur
            
        But : Appeller la vue permettant d'ajouter une interface
        
        Fonctionnement : Fermer la fenêtre courante puis lancer la vue chargée d'ajouter une interface.
        '''        
        self.close()
        self.vueAjouterInterface(myCtrl,nomRouteur)

    def btn_clickDeleteInterface(self,myCtrl,nomRouteur):   
        '''
        Paramètres :
            - myCtrl (Controller) : instance de la classe Controller            
            - nomRouteur (String) : nom du routeur
            
        But : Supprimer une interface en appellant les fonctions deleteInterface et sshChangeInterface
        
        Fonctionnement : Appeller la fonction deleteInterface pour chaque checkBox (le tri se fera dans cette fonction)
                         puis appel la fonction sshChangeInterface. Enfin, on ferme la fenêtre courante et on appelle
                         la vue de l'accueil des interfaces.
        ''' 
        global nomFichier
       
        for items in self.findChildren(QRadioButton):
            myCtrl.deleteInterface(nomFichier,nomRouteur,items)
           
        myCtrl.sshChangeInterface(nomFichier,nomRouteur)
              
        self.close()
        self.accueilInterface(myCtrl, nomRouteur)


       
    def btn_clickSelectInterface(self,myCtrl,nomRouteur):
        '''
        Paramètres :
            - myCtrl (Controller) : instance de la classe Controller            
            - nomRouteur (String) : nom du routeur
            
        But : Afficher la vue de configuration d'une interferface. Si aucune interface n'est choisi, appeller la
              vue de l'accueil des interfaces.
        
        Fonctionnement : Fermer la fenêtre courante. Vérifier quel checkbox est coché puis appeller la fonction 
                         selectInterface pour récupérer les informations liées au nom de l'interface. Puis appeller
                         la vue de configuration d'une interface avec les bons paramètres. 
        ''' 
        
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
        '''
        Paramètres :
            - myCtrl (Controller) : instance de la classe Controller            
            - nomRouteur (String) : nom du routeur
            
        But : Effectuer la sauvegarde de la nouvelle interface en question via l'appel des fonctions 
              addSaveInterface et sshChangeInterface.
        
        Fonctionnement : Appeler la fonction addSaveInterface et sshChangeInterface. Puis fermer la 
              fenêtre courante et lancer la vue de l'accueil des interfaces.
        '''        
        global nomFichier
       
        textLe1 = self.le1.text()
        textLe2 = self.le2.text()
        textLe3 = self.le3.text()
        textLe4 = self.le4.text()
       
        myCtrl.addSaveInterface(nomFichier,nomRouteur,textLe1,textLe2,textLe3,textLe4)
       
        myCtrl.sshChangeInterface(nomFichier,nomRouteur)

       
        self.close()    
        self.accueilInterface(myCtrl,nomRouteur)

 
    def btn_clickEditSaveInterface(self,myCtrl, nomRouteur,nomInterface,adresseIP,masque,passerelleDefaut):
        '''
        Paramètres :
            - myCtrl (Controller) : instance de la classe Controller            
            - nomRouteur (String) : nom du routeur
            - nomInterface (String) : nom de l'interface
            - adresseIP (String) : adresse IP de l'interface
            - masque (String) : masque de l'interface
            - passerelleDefaut (String) : passerelle par defaut de l'interface
            
        But : Effectuer la sauvegarde des modifications sur l'interface en question via l'appel des fonctions 
              editSaveInterface et sshChangeInterface.
        
        Fonctionnement : Appeler la fonction editSaveInterface et sshChangeInterface. Puis fermer la 
              fenêtre courante et lancer la vue de l'accueil des interfaces.
        '''         
        global nomFichier
       
        myCtrl.editSaveInterface(nomFichier,nomRouteur,nomInterface,adresseIP,masque,passerelleDefaut)
                          
        myCtrl.sshChangeInterface(nomFichier,nomRouteur)
       
        self.close()
        self.accueilInterface(myCtrl,nomRouteur)


    def btn_clickCancelInterface(self,myCtrl,nomRouteur): 
        '''
        Paramètres : 
            - myCtrl (Controller) : instance de la classe Controller
            - nomRouteur (String) : nom du routeur choisi
            
        But : Fonction permettant d'annuler l'enregistrement, la modification et l'ajout d'une interface.
        
        Fonctionnement : Fermer la fenêtre courante puis lancer la vue de l'accueil des interfaces.
        '''        
        self.close()
        self.accueilInterface(myCtrl,nomRouteur)
     
        
     
    def saveDb(self):
        '''            
        But : Fonction permettant de sauvegarder les configurations faites sur l'application.
        
        Fonctionnement : Faire appel à la fonction getSaveFileName pour affichier la fenêtre de sauvegarde d'un
                         fichier. Puis copier/coller le fichier avec le nouveau nom. En cas d'erreur, on ne fait
                         rien.
        '''        
        try:
            savName = QFileDialog.getSaveFileName(self, 'Sauvegarder fichier','c:\\',"Data files (*.csv)")
            global nomFichier
            shutil.copyfile(nomFichier, savName[0])
        except FileNotFoundError:
            pass
           
           
       
    def openDb(self,myCtrl):
        '''
        Paramètres : 
            - myCtrl (Controller) : instance de la classe Controller
            
        But : Fonction permettant d'ouvrir un fichier existant pour l'importer dans l'application.
        
        Fonctionnement : Faire appel à la fonction getOpenFileName pour affichier la fenêtre d'ouverture d'un
                         fichier. Puis fermer la fenêtre et lancer la vue de l'accueil. En cas d'erreur, on fixe le nom
                         du fichier par defaut et on lance la vue de l'accueil.
        '''       
        global nomFichier
        try:
            fname = QFileDialog.getOpenFileName(self, 'Ouvrir fichier','G:/EPISEN/ITS 1/S2/IHM/Projet/Test solo/',"Data files (*.csv)")          
            nomFichier = fname[0]
            self.close()
            self.__init__(myCtrl)
        except FileNotFoundError:
            nomFichier = 'database.csv'
            self.__init__(myCtrl)
           
           
           
#=========== ROUTE ===========#   

    def vueAddRoute(self,myCtrl,nomRouteur, parent = None):
        '''
        Paramètres : 
            - myCtrl (Controller) : instance de la classe Controller
            - nomRouteur (String) : nom du routeur
            
        But : Fonction qui met en place la vue permettant d'ajouter une route.
        '''          
        # Héritage - appel à la classe mère
        super(View, self).__init__(parent)		
       
        # Mise en place du layout
        self.layout = QFormLayout()

        # Mise en place des widgets 
        self.text1 = QLabel("Destination : ")
        self.le1 = QLineEdit()
        self.layout.addRow(self.text1,self.le1)
      
        self.text2 = QLabel("Masque : ")
        self.le2 = QLineEdit()
        self.layout.addRow(self.text2,self.le2)
      
        self.text3 = QLabel("Via : ")
        self.le3 = QLineEdit()
        self.layout.addRow(self.text3,self.le3)
            
        self.buttonSaveRoute = QPushButton("Ajouter la route")
        self.buttonSaveRoute.setIcon(QIcon('Logo\plus.svg'))        
        self.buttonCancelRoute = QPushButton("Annuler")
        self.buttonCancelRoute.setIcon(QIcon('Logo\exit.svg'))
        
        self.layout.addRow(self.buttonSaveRoute, self.buttonCancelRoute)
        self.setLayout(self.layout)
       
        # Gestion des events
        self.buttonSaveRoute.clicked.connect(lambda: self.btn_clickAddRoute(myCtrl,nomRouteur,self.le1.text(),self.le2.text(),self.le3.text()))
        self.buttonCancelRoute.clicked.connect(lambda: self.btn_clickCancelRoute(myCtrl,nomRouteur))
       
       
        self.setWindowTitle("Ajouter une interface")
        self.show()


    def vueDeleteRoute(self,myCtrl,nomRouteur, parent = None):
        '''
        Paramètres : 
            - myCtrl (Controller) : instance de la classe Controller
            - nomRouteur (String) : nom du routeur
            
        But : Fonction qui met en place la vue permettant de supprimer une route.
        '''        
        # Héritage - appel à la classe mère
        super(View, self).__init__(parent)		
       
        # Mise en place du layout
        self.layout = QFormLayout()

        # Mise en place des widgets 
        self.text1 = QLabel("Destination : ")
        self.le1 = QLineEdit()
        self.layout.addRow(self.text1,self.le1)
      
        self.text2 = QLabel("Masque : ")
        self.le2 = QLineEdit()
        self.layout.addRow(self.text2,self.le2)
      
        self.text3 = QLabel("Via : ")
        self.le3 = QLineEdit()
        self.layout.addRow(self.text3,self.le3)
            
        self.buttonDeleteRoute = QPushButton("Supprimer la route")
        self.buttonCancelRoute.setIcon(QIcon('Logo\trash.svg'))        
        self.buttonCancelRoute = QPushButton("Annuler")
        self.buttonCancelRoute.setIcon(QIcon('Logo\exit.svg'))
        
        self.layout.addRow(self.buttonDeleteRoute, self.buttonCancelRoute)
        self.setLayout(self.layout)
       
        # Gestion des events
        self.buttonDeleteRoute.clicked.connect(lambda: self.btn_clickDeleteRoute(myCtrl,nomRouteur,self.le1.text(),self.le2.text(),self.le3.text()))
        self.buttonCancelRoute.clicked.connect(lambda: self.btn_clickCancelRoute(myCtrl,nomRouteur))
       
       
        self.setWindowTitle("Ajouter une interface")
        self.show()
        
    def btn_clickCancelRoute(self,myCtrl,nomRouteur):  
        '''
        Paramètres : 
            - myCtrl (Controller) : instance de la classe Controller
            - nomRouteur (String) : nom du routeur
            
        But : Fonction qui ferme la fenetre courante et lance la fenetre d'accueil des interfaces.
        '''          
        self.close()
        self.accueilInterface(myCtrl,nomRouteur)

    def btn_clickAddRoute(self,myCtrl,nomRouteur,destination,masque,via): 
        '''
        Paramètres : 
            - myCtrl (Controller) : instance de la classe Controller
            - nomRouteur (String) : nom du routeur
            - destination (String) : destination de la route que l'on va créer
            - masque (String) : masque de la route que l'on va créer
            - via (String) : passerelle par défaut de la route que l'on va créer
            
        But : Fonction qui appelle la fonction sshAddRoute, ferme la fenetre courante et lance la fenetre
              d'accueil des interfaces.
        '''        
        global nomFichier
       
        myCtrl.sshAddRoute(nomFichier,nomRouteur,destination,masque,via)

       
        self.close()
        self.accueilInterface(myCtrl,nomRouteur)


    def btn_clickDeleteRoute(self,myCtrl,nomRouteur,destination,masque,via):
        '''
        Paramètres : 
            - myCtrl (Controller) : instance de la classe Controller
            - nomRouteur (String) : nom du routeur
            - destination (String) : destination de la route que l'on va créer
            - masque (String) : masque de la route que l'on va créer
            - via (String) : passerelle par défaut de la route que l'on va créer
            
        But : Fonction qui appelle la fonction sshDelRoute, ferme la fenetre courante et lance la fenetre
              d'accueil des interfaces.
        ''' 
        
        global nomFichier
       
        myCtrl.sshDelRoute(nomFichier,nomRouteur,destination,masque,via)

        self.close()
        self.accueilInterface(myCtrl,nomRouteur)


        
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