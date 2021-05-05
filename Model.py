# -*- coding:utf-8 -*-
"""
Created on Tue Apr 02 14:50:31 2021

@author: Thomas
"""



#============== MODEL ==============#

class Model:

    def deleteRouteur(self,nomFichier,items):
        '''
        Paramètres : 
            - nomFichier (String) : nom du fichier où les informations seront enregistrées
            - items (Objet QRadioButton) :  objet QRadioButton courant
            
        But : Fonction permettant de supprimer le routeur choisi.
        
        Fonctionnement : Réécrire le fichier sans la ligne du fichier correspondant 
                         au routeur en question.
        '''
        if items.isChecked():
            with open(nomFichier,'r') as f:
                lines = f.readlines()
            with open(nomFichier,'w') as f2:
                for line in lines:
                    if line.split(',')[0] != items.text():
                        f2.write(line)


    def addSaveRouteur(self, nomFichier, text1,text2,text3):
        '''
        Paramètres : 
            - nomFichier (String) : nom du fichier où les informations seront enregistrées
            - text1 (String) : nom du routeur
            - text2 (String) : adresse IP du routeur
            - text3 (String) : masque du routeur
            
        But : Fonction permettant d'ajouter un routeur.
        
        Fonctionnement : Ecrire dans le fichier les infos du nouveau routeur.
        '''        
        with open(nomFichier, 'a') as f:
           f.write(text1 + "," + text2 + "," + text3 + "," + "eth0" + "," + text2 + "," + text3 + "," + text2 + "," + "\n")
 
           
    def editSaveRouteur(self,nomFichier,nomRouteur,adresseIP,masque):
        '''
        Paramètres : 
            - nomFichier (String) : nom du fichier où les informations seront enregistrées
            - nomRouteur (String) : nom du routeur
            - adresseIP (String) : adresse IP du routeur
            - masque (String) : masque du routeur
            
        But : Fonction permettant de modifier un routeur.
        
        Fonctionnement : Ecrire dans le fichier les nouvelles infos du routeur en
                         construisant la ligne avec les nouvelles infos + infos non 
                         modifiées.
        '''         
        with open(nomFichier, 'r') as f:
            lignes = f.readlines()
            compteur =0
            for ligneCourante in lignes:
                if(ligneCourante.split(',')[0] == nomRouteur):
                    debut = list()
                    debut.extend([nomRouteur, adresseIP,masque])
                    fin = ligneCourante.split(',')[3:]
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
                
  
                
    def deleteInterface(self,nomFichier,nomRouteur,items):
        '''
        Paramètres : 
            - nomFichier (String) : nom du fichier où les informations seront enregistrées
            - nomRouteur (String) : nom du routeur
            - items (Objet QRadioButton) :  objet QRadioButton courant
            
        But : Fonction permettant de supprimer l'interface choisie.
        
        Fonctionnement : Réécrire le fichier sans les informations de l'interface 
                         en question construisant la ligne sans les infos de l'interface
                         mais avec les autres informations.
        '''        
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
 
                
    def addSaveInterface(self,nomFichier,nomRouteur,nomInterface,adresseIP,masque,passerelleDefaut):
        '''
        Paramètres : 
            - nomFichier (String) : nom du fichier où les informations seront enregistrées
            - nomRouteur (String) : nom du routeur
            - nomInterface (String) : nom de l'interface
            - adresseIP (String) : adresse IP de l'interface
            - masque (String) : masque de l'interface
            - passerelleDefaut (String) : passerelle par defaut de l'interface
            
        But : Fonction permettant d'ajouter une interface.
        
        Fonctionnement : Ajouter les informations de l'interface à la suite de la ligne
                         du routeur possèdant l'interface.
        '''        
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
                ligneSplit.extend([nomInterface,adresseIP,masque,passerelleDefaut+"\n"])    
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

                
    def editSaveInterface(self,nomFichier,nomRouteur,nomInterface,adresseIP,masque,passerelleDefaut):
        '''
        Paramètres : 
            - nomFichier (String) : nom du fichier où les informations seront enregistrées
            - nomRouteur (String) : nom du routeur possédant l'interface
            - nomInterface (String) : nom de l'interface modifiée
            - adresseIP (String) : adresse IP de l'interface modifiée
            - masque (String) : masque de l'interface modifiée
            - passerelleDefaut (String) : passerelle par defaut de l'interface modifiée
            
        But : Fonction permettant de modifier les informations d'une interface.
        
        Fonctionnement : Modifier les informations de l'interface à l'endroit où elles
                         se trouvaient initialement.
        '''           
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
                    

    def editRouteur(self,nomFichier,items):
        '''
        Paramètres : 
            - nomFichier (String) : nom du fichier où les informations seront enregistrées
            - items (Objet QRadioButton) :  objet QRadioButton courant
            
        But : Fonction permettant de récupérer les informations du routeur que l'on
              souhaite modifier.
        
        Fonctionnement : Renvoie les nouvelles informations modifiées afin de les passer
                         à la vue gérant l'affichage de l'interface.
        '''        
        isCheck = False
        with open(nomFichier,'r') as f:
            lines = f.readlines()
            for line in lines:
                if(line.split(',')[0] == items.text()):
                    isCheck = True
                    nomRouteur = items.text()
                    adresseIP = line.split(',')[1]
                    masque = line.split(',')[2]
                    return isCheck,nomRouteur,adresseIP,masque 
 
                          
    def findInfoRouteur(self,nomFichier,nomRouteur):
        '''
        Paramètres : 
            - nomFichier (String) : nom du fichier où les informations seront enregistrées
            - nomRouteur (String) :  nom du routeur choisi
            
        But : Fonction permettant de retourner les informations d'un routeur passé en paramètre.
        
        Fonctionnement : Parcourir ligne par ligne le fichier passé en paramètre et retourner la ligne
                         avec le nom du routeur passé lui aussi en paramètre.
        '''        
        with open(nomFichier,'r') as f:
            lines = f.readlines()
            for line in lines:
                if(line.split(',')[0] == nomRouteur):
                    return line.split(',')
                           
                           
    def selectInterface(self,nomFichier,nomRouteur,items):
        '''
        Paramètres : 
            - nomFichier (String) : nom du fichier où les informations seront enregistrées
            - items (Objet QRadioButton) :  objet QRadioButton courant
            
        But : Fonction permettant de récupérer les informations liées à l'interface 
              choisie.
        
        Fonctionnement : Renvoie les informations de l'interface choisie à la vue gérant
                         cet affichage.
        ''' 
        isCheck = False
        with open(nomFichier,'r') as f:
                   lignes = f.readlines()                  
                   for ligneCourante in lignes:
                       if(ligneCourante.split(',')[0] == nomRouteur):                         
                           try:
                               isCheck = True
                               index = ligneCourante.split(',').index(items.text())
                               nomInterface = items.text()
                               adresseIP = ligneCourante.split(",")[index+1]
                               masque = ligneCourante.split(",")[index+2]
                               passerelleDefaut = ligneCourante.split(",")[index+3]
                               
                               return isCheck,nomInterface,adresseIP,masque,passerelleDefaut
                               
                           except IndexError:
                               pass
                           
                           
                           