import sys, csv, shutil
from PyQt5.QtWidgets import (QLineEdit, QTableWidget, QInputDialog, QPushButton, QVBoxLayout, QHBoxLayout,
                             QApplication,qApp, QRadioButton, QMenuBar, QFileDialog, QFormLayout, QMainWindow, qApp, QGridLayout, QAction, QWidget,QLabel,QRadioButton)
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore


class inputdialogdemo(QWidget):
    
   def __init__(self, parent = None):
       global nomFichier
       
       super(inputdialogdemo, self).__init__(parent)
       
       self.layout = QFormLayout()
       self.menu = QMenuBar()
       self.menuFichier = self.menu.addMenu("Fichier") 
       self.layout.addRow(self.menu)

      
       # Création sous menu Ouvrir
       ouvrirMenu = QAction(QIcon('open.svg'),'Ouvrir', self)
       ouvrirMenu.setShortcut('Ctrl+O')
       ouvrirMenu.triggered.connect(self.openDb)
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
       
              
       self.buttonAdd = QPushButton("Ajouter un routeur")
       self.buttonSelect = QPushButton("Voir le routeur")
       self.buttonDelete = QPushButton("Supprimer le routeur")

           
       self.layout.addRow(self.buttonSelect)
       self.layout.addRow(self.buttonAdd,self.buttonDelete)
       
       

       self.setLayout(self.layout)
       

       if not self.findChildren(QRadioButton):
           self.buttonSelect.setEnabled(False)
           self.buttonDelete.setEnabled(False)

       
       
       
       self.buttonSelect.clicked.connect(self.btn_clickSelectRouteur)
       self.buttonAdd.clicked.connect(self.btn_clickAddRouteur)
       self.buttonDelete.clicked.connect(self.btn_clickDeleteRouteur)
       
       self.setWindowTitle("Accueil")
       self.show()
       
       
       

   def ajouterRouteur(self, parent = None):
       super(inputdialogdemo, self).__init__(parent)		
       self.layout = QFormLayout()

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
       
       self.buttonSave.clicked.connect(self.btn_clickAddSaveRouteur)
       self.buttonCancel.clicked.connect(self.btn_clickCancelRouteur)
       self.layout.addRow(self.buttonSave, self.buttonCancel)
       
       self.setLayout(self.layout)
       self.setWindowTitle("Ajouter un routeur")

       self.show()
       
   def configRouteur(self, nomRouteur, adresseIP,masque, parent = None):
       super(inputdialogdemo, self).__init__(parent)		
       

       self.layout = QFormLayout()            
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
       
       self.buttonSaveRouteur.clicked.connect(lambda: self.btn_clickEditSaveRouteur(self.le1.text(),self.le2.text(),self.le3.text(),self.le4.text()))
       self.buttonCancelRouteur.clicked.connect(self.btn_clickCancelRouteur)
       self.layout.addRow(self.buttonSaveRouteur, self.buttonCancelRouteur)
       
       self.setLayout(self.layout)
       self.setWindowTitle("Configuration du routeur : " + nomRouteur)

       self.show()
       
       
       
   def btn_clickDeleteRouteur(self):   
       global nomFichier
       
       for items in self.findChildren(QRadioButton):
           if items.isChecked():
               with open(nomFichier,'r') as f:
                   lines = f.readlines()
               with open(nomFichier,'w') as f2:
                   for line in lines:
                       if line.split(',')[0] != items.text():
                           f2.write(line)                  
       self.close()
       self.__init__()


   def btn_clickSelectRouteur(self):
       self.close()
       for items in self.findChildren(QRadioButton):
           if items.isChecked():
               nomRouteur = items.text()
       self.accueilInterface(nomRouteur)
       


   def btn_clickAddRouteur(self):
       self.close()
       self.ajouterRouteur()


   def btn_clickCancelRouteur(self):   
       self.close()
       self.__init__()


   def btn_clickAddSaveRouteur(self):
       global nomFichier
       
       textLe1 = self.le1.text()
       textLe2 = self.le2.text()
       textLe3 = self.le3.text()
       
       with open(nomFichier, 'a') as f:
           f.write(textLe1 + "," + textLe2 + "," + textLe3 + "\n")
       
       self.close()    
       self.__init__()

 
   def btn_clickEditSaveIRouteur(self,nomRouteur,adresseIP,masque):
       global nomFichier
       with open(nomFichier, 'r') as f:
           lignes = f.readlines()
           index =0
       for ligneCourante in lignes:
           if(ligneCourante.split(',')[0] == nomRouteur):
               lignes[index] = nomRouteur + "," + adresseIP + "," + masque + "\n"
           index += 1
       with open(nomFichier, 'w') as f:
           f.writelines(lignes)

       self.close()
       self.__init__()







#           INTERFACE

   def accueilInterface(self,nomRouteur,parent = None):
       global nomFichier
       
       super(inputdialogdemo, self).__init__(parent)
       
       self.layout = QFormLayout()
       self.menu = QMenuBar()
       self.menuFichier = self.menu.addMenu("Fichier") 
       self.layout.addRow(self.menu)

      
       # Création sous menu Ouvrir
       ouvrirMenu = QAction(QIcon('open.svg'),'Ouvrir', self)
       ouvrirMenu.setShortcut('Ctrl+O')
       ouvrirMenu.triggered.connect(self.openDb)
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
       
       
       self.tableRoutage = QTableWidget(5,3)
       self.tableRoutage.setHorizontalHeaderLabels(['Destination réseau', 'Masque réseau', 'Adresse passerelle'])
       
       self.buttonAdd = QPushButton("Ajouter une interface")
       self.buttonSelect = QPushButton("Voir l'interface")
       self.buttonDelete = QPushButton("Supprimer l'interface")
       self.buttonBackHome = QPushButton("Revenir à l'accueil")

       self.layout.addRow(self.tableRoutage)    
       self.layout.addRow(self.buttonSelect)
       self.layout.addRow(self.buttonAdd,self.buttonDelete)
       self.layout.addRow(self.buttonBackHome)
       
       
       self.setLayout(self.layout)
       

       if not self.findChildren(QRadioButton):
           self.buttonSelect.setEnabled(False)
           self.buttonDelete.setEnabled(False)

       
       self.buttonSelect.clicked.connect(lambda: self.btn_clickSelectInterface(nomRouteur))
       self.buttonAdd.clicked.connect(lambda: self.btn_clickAddInterface(nomRouteur))
       self.buttonDelete.clicked.connect(lambda: self.btn_clickDeleteInterface(nomRouteur))
       self.buttonBackHome.clicked.connect(self.btn_clickBackHome)

       
       self.setWindowTitle("Choix interface du routeur : " + nomRouteur)
       self.show()
       
       

   def ajouterInterface(self,nomRouteur, parent = None):
       super(inputdialogdemo, self).__init__(parent)		
       self.layout = QFormLayout()

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
       
       self.buttonSave.clicked.connect(lambda: self.btn_clickAddSaveInterface(nomRouteur))
       self.buttonCancel.clicked.connect(self.btn_clickCancelInterface)
       self.layout.addRow(self.buttonSave, self.buttonCancel)
       
       self.setLayout(self.layout)
       self.setWindowTitle("Ajouter une interface")

       self.show()
       
   def configInterface(self, nomRouteur, nomInterface, adresseIP, masque, passerelleDefaut, parent = None):
       super(inputdialogdemo, self).__init__(parent)		
       

       self.layout = QFormLayout()            
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
       
       self.buttonSaveInterface.clicked.connect(lambda: self.btn_clickEditSaveInterface(nomRouteur,self.le1.text(),self.le2.text(),self.le3.text(),self.le4.text()))
       self.buttonCancelInterface.clicked.connect(lambda: self.btn_clickCancelInterface(nomRouteur))
       self.layout.addRow(self.buttonSaveInterface, self.buttonCancelInterface)
       
       self.setLayout(self.layout)
       self.setWindowTitle("Configuration de l'interface : " + nomInterface)

       self.show()
      

       
   def btn_clickBackHome(self):
       self.close()
       self.__init__()

   def btn_clickAddInterface(self,nomRouteur):
       self.close()
       self.ajouterInterface(nomRouteur)

   def btn_clickDeleteInterface(self,nomRouteur):   
       global nomFichier
       
       for items in self.findChildren(QRadioButton):
           if items.isChecked():
               with open(nomFichier,'r') as f:
                   lines = f.readlines()
                   compteur =  0
                   for line in lines:
                       if(line.split(',')[0] == nomRouteur):
                           index = line.split(',').index(items.text())
                           debut = line.split(',')[:index]
                           fin = line.rstrip('\n').split(',')[index+4:]
                           debut.extend(fin)
                           debut.extend("\n")
                           nbLigne = compteur
                       compteur += 1
             
               with open(nomFichier, 'w') as f:
                    compteur2 = 0
                    for ligne in lines:
                        if(compteur2 == nbLigne):
                            f.writelines(",".join(debut))
                        else:
                            f.writelines(ligne)
                        compteur2 +=1
       self.close()
       self.accueilInterface(nomRouteur)


       
   def btn_clickSelectInterface(self,nomRouteur):
       global nomFichier
       self.close()
       indicateur = False
       for items in self.findChildren(QRadioButton):
           if items.isChecked():
               indicateur = True
               with open(nomFichier,'r') as f:
                   lignes = f.readlines()
                   
                   for ligneCourante in lignes:
                       if(ligneCourante.split(',')[0] == nomRouteur):                         
                           try:
                               
                               index = ligneCourante.split(',').index(items.text())
                               nomInterface = items.text()
                               adresseIP = ligneCourante.split(",")[index+1]
                               masque = ligneCourante.split(",")[index+2]
                               passerelleDefaut = ligneCourante.split(",")[index+3]
                               
                               self.configInterface(nomRouteur,nomInterface,adresseIP,masque,passerelleDefaut)
                               
                           except IndexError:
                               pass
       # Si aucun bouton radio est check mais qu'on appuie quand meme sur "Sélectionner"               
       if indicateur == False:
           self.accueilInterface(nomRouteur) 
                   
               
   def btn_clickAddSaveInterface(self,nomRouteur):
       global nomFichier
       
       textLe1 = self.le1.text()
       textLe2 = self.le2.text()
       textLe3 = self.le3.text()
       textLe4 = self.le4.text()
       with open(nomFichier, 'r') as f:
           lignes = f.readlines()
           compteur =0
       for ligneCourante in lignes:
           if(ligneCourante.split(',')[0] == nomRouteur):
               ligneSplit = ligneCourante.split(',')
               ligneSplit = [i for i in ligneSplit if i != '']
               ligneSplit = [i for i in ligneSplit if i != '\n']
               
               for i in range(len(ligneSplit)):
                   ligneSplit[i] = ligneSplit[i].rstrip('\n')
               ligneSplit.extend([textLe1,textLe2,textLe3,textLe4,"\n"])    
               nbLigne = compteur
               
           compteur += 1
       with open(nomFichier, 'w') as f:
           compteur2 = 0
           for ligne in lignes:
               if(compteur2 == nbLigne):
                   f.writelines(",".join(ligneSplit))
               else:
                   f.writelines(ligne)
               compteur2 +=1
       
       self.close()    
       self.accueilInterface(nomRouteur)

 
   def btn_clickEditSaveInterface(self,nomRouteur,nomInterface,adresseIP,masque,passerelleDefaut):
       global nomFichier
       with open(nomFichier, 'r') as f:
           lignes = f.readlines()
           compteur =0
       for ligneCourante in lignes:
           if(ligneCourante.split(',')[0] == nomRouteur):
               index = ligneCourante.split(',').index(nomInterface)
               debut = ligneCourante.split(',')[:index]
               fin = ligneCourante.split(',')[index+4:]
               debut.extend([nomInterface, adresseIP,masque,passerelleDefaut])
               debut.extend(fin)
               nbLigne = compteur
            
           compteur += 1
       with open(nomFichier, 'w') as f:
           compteur2 = 0
           for ligne in lignes:
               if(compteur2 == nbLigne):
                   f.writelines(",".join(debut))
               else:
                   f.writelines(ligne)
               compteur2 +=1

       self.close()
       self.accueilInterface(nomRouteur)

   def btn_clickCancelInterface(self,nomRouteur):   
       self.close()
       self.accueilInterface(nomRouteur)
     
        
     
        
     
        
   def saveDb(self):
       try:
           savName = QFileDialog.getSaveFileName(self, 'Sauvegarder fichier','c:\\',"Data files (*.csv)")
           global nomFichier
           shutil.copyfile(nomFichier, savName[0])
       except FileNotFoundError:
           pass
           
           
       
   def openDb(self,nomRouteur):
       global nomFichier
       try:         
           fname = QFileDialog.getOpenFileName(self, 'Ouvrir fichier','G:/EPISEN/ITS 1/S2/IHM/Projet/Test solo/',"Data files (*.csv)")          
           nomFichier = fname[0]
           self.close()
           self.__init__()
       except FileNotFoundError:
           nomFichier = 'database.csv'
           self.__init__()
           
           
   

       
	
if __name__ == '__main__':
   app = QApplication(sys.argv)
   global compteur 
   compteur = 1
   global nomFichier
   nomFichier = 'database.csv'
   creationFichier = open(nomFichier, 'w')
   ex = inputdialogdemo()
   sys.exit(app.exec_())