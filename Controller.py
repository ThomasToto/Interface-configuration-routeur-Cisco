# -*- coding:utf-8 -*-
"""
Created on Tue Apr 02 14:51:55 2021

@author: Thomas
"""


#=========== IMPORTATION ===========#

import paramiko

#===================================#



#============== CONTROLLER ===============#

class Controller:
    def __init__(self, model):
        '''
        Paramètres : 
            - model (Model) : instance de la classe Model
            
        But : Fonction permettant d'initialiser une instance de la classe Controller.       
        '''    
        
        self.myModel = model
        
    def deleteRouteur(self,nomFichier,items):
        '''
        Paramètres : 
            - nomFichier (String) : nom du fichier où les informations seront enregistrées
            - nomRouteur (String) : nom du routeur
            
        But : Fonction permettant d'appeller la fonction deleteRouteur du Model.        
        '''     
        
        self.myModel.deleteRouteur(nomFichier,items)
        
    def addSaveRouteur(self,nomFichier, text1,text2,text3):
        '''
        Paramètres : 
            - nomFichier (String) : nom du fichier où les informations seront enregistrées
            - text1 (String) : nom du routeur
            - text2 (String) : adresse IP du routeur
            - text3 (String) : masque du routeur
            
        But : Fonction permettant d'appeller la fonction addSaveRouteur du Model.        
        '''      
        
        self.myModel.addSaveRouteur(nomFichier,text1,text2,text3)
        
        
    def editSaveRouteur(self,nomFichier,nomRouteur,adresseIP,masque):
        '''
        Paramètres : 
            - nomFichier (String) : nom du fichier où les informations seront enregistrées
            - nomRouteur (String) : nom du routeur
            - adresseIP (String) : adresse IP du routeur
            - masque (String) : masque du routeur
            
        But : Fonction permettant d'appeller la fonction editSaveRouteur du Model.      
        '''   
        
        self.myModel.editSaveRouteur(nomFichier,nomRouteur,adresseIP,masque)
        
        
    def deleteInterface(self,nomFichier,nomRouteur,items):
        '''
        Paramètres : 
            - nomFichier (String) : nom du fichier où les informations seront enregistrées
            - nomRouteur (String) : nom du routeur
            - items (Objet QRadioButton) :  objet QRadioButton courant
            
        But : Fonction permettant d'appeller la fonction deleteInterface du Model.        
        '''       
        
        self.myModel.deleteInterface(nomFichier,nomRouteur,items)
        
        
    def addSaveInterface(self,nomFichier,nomRouteur,nomInterface,adresseIP,masque,passerelleDefaut):
        '''
        Paramètres : 
            - nomFichier (String) : nom du fichier où les informations seront enregistrées
            - nomRouteur (String) : nom du routeur
            - nomInterface (String) : nom de l'interface
            - adresseIP (String) : adresse IP de l'interface
            - masque (String) : masque de l'interface
            - passerelleDefaut (String) : passerelle par défaut de l'interface
            
        But : Fonction permettant d'appeller la fonction addSaveInterface du Model.       
        '''      
        
        self.myModel.addSaveInterface(nomFichier,nomRouteur,nomInterface,adresseIP,masque,passerelleDefaut)

    def editSaveInterface(self,nomFichier,nomRouteur,nomInterface,masque,adresseIP,passerelleDefaut):
        '''
        Paramètres : 
            - nomFichier (String) : nom du fichier où les informations seront enregistrées
            - nomRouteur (String) : nom du routeur
            - nomInterface (String) : nom de l'interface
            - masque (String) : adresse IP de l'interface
            - adresseIP (String) : masque de l'interface
            - passerelleDefaut (String) : passerelle par défaut de l'interface
            
        But : Fonction permettant d'appeller la fonction editSaveInterface du Model.      
        '''       
        
        self.myModel.editSaveInterface(nomFichier,nomRouteur,nomInterface,masque,adresseIP,passerelleDefaut)

    def editRouteur(self,nomFichier,items):
        '''
        Paramètres : 
            - nomFichier (String) : nom du fichier où les informations seront enregistrées
            - items (Objet QRadioButton) :  objet QRadioButton courant
            
        But : Fonction permettant retourner la fonction editRouteur du Model.        
        '''      
        
        return self.myModel.editRouteur(nomFichier,items)

    def selectInterface(self,nomFichier,nomRouteur,items):
        '''
        Paramètres : 
            - nomFichier (String) : nom du fichier où les informations seront enregistrées
            - nomRouteur (String) : nom du routeur            
            - items (Objet QRadioButton) :  objet QRadioButton courant
            
        But : Fonction permettant retourner la fonction selectInterface du Model.      
        '''   
        
        return self.myModel.selectInterface(nomFichier,nomRouteur,items)
    
    def findInfoRouteur(self,nomFichier,nomRouteur):
        '''
        Paramètres : 
            - nomFichier (String) : nom du fichier où les informations seront enregistrées
            - nomRouteur (String) : nom du routeur            
            
        But : Fonction permettant retourner la fonction findInfoRouteur du Model.      
        ''' 
        
        return self.myModel.findInfoRouteur(nomFichier,nomRouteur)
    
    
    def sshChangeInterface(self,nomFichier,nomRouteur):
        '''
        Paramètres : 
            - nomFichier (String) : nom du fichier où les informations seront enregistrées
            - nomRouteur (String) : nom du routeur
            
        But : Fonction permettant de modifier les interfaces du routeur
        
        Fonctionnement : Effectuer une connexion en ssh sur l'adresse IP du routeur. Désactiver les cartes réseaux.
                         Réécrire en entier le fichier avec les nouvelles informations sur les interfaces
                         du routeur. Activer les cartes réseaux. On ne modifie pas la première interface car c'est
                         l'interface sur laquelle on va se connecter en ssh.
        '''     
        
        reponse = self.findInfoRouteur(nomFichier,nomRouteur)
        
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(reponse[1], username="root", password="vitrygtr")
        
        
        text = ""
        for i in range(3,len(reponse)-1,4):
            if(i != 3):
                client.exec_command("sudo ifdown "+reponse[i].rstrip("\n"))
            text += "\nauto "+ reponse[i].rstrip("\n") +"\n"
            text += "iface " + reponse[i].rstrip("\n") + " inet static \n"
            text += "address " + reponse[i+1].rstrip("\n") + "\n"
            text += "netmask " + reponse[i+2].rstrip("\n") + "\n"
            text += "gateway " + reponse[i+3].rstrip("\n") + "\n"
        stdin, stdout, stderr = client.exec_command("sudo echo \""+text+"\" > /etc/network/interfaces")
        for i in range(3,len(reponse)-1,4):
            if(i != 3):
                client.exec_command("sudo ifup "+reponse[i].rstrip("\n"))
        
    def sshShowRoute(self,nomFichier,nomRouteur):
        '''
        Paramètres : 
            - nomFichier (String) : nom du fichier où les informations seront enregistrées
            - nomRouteur (String) : nom du routeur
            
        But : Fonction permettant d'afficher la table de routage du routeur choisi.
        
        Fonctionnement :  Effectuer une connexion en ssh sur l'adresse IP du routeur. Effectuer la commande
                          "route -n" puis récupérer la sortie de cette commande. 
        '''    
        
        reponse = self.findInfoRouteur(nomFichier,nomRouteur)
        
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(reponse[1], username="root", password="vitrygtr")
        stdin, stdout, stderr = client.exec_command("route -n")
        route = ''.join(stdout.readlines())
        return route
     
    def sshDisableRoutage(self,nomFichier,nomRouteur):
        '''
        Paramètres : 
            - nomFichier (String) : nom du fichier où les informations seront enregistrées
            - nomRouteur (String) : nom du routeur
            
        But : Fonction permettant de désactiver le routeur passé en paramètre.
        
        Fonctionnement :  Effectuer une connexion en ssh sur l'adresse IP du routeur. Effectuer la commande
                          "echo 0" puis retourner la sortie de cette commande vers le fichier
                          /proc/sys/net/ipv4/ip_forward
        '''      
        
        reponse = self.findInfoRouteur(nomFichier,nomRouteur)
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(reponse[1], username="root", password="vitrygtr")
        client.exec_command("echo 0 | sudo tee /proc/sys/net/ipv4/ip_forward")
    
    def sshEnableRoutage(self,nomFichier,nomRouteur):   
        '''
        Paramètres : 
            - nomFichier (String) : nom du fichier où les informations seront enregistrées
            - nomRouteur (String) : nom du routeur
            
        But : Fonction permettant de désactiver le routeur passé en paramètre.
        
        Fonctionnement :  Effectuer une connexion en ssh sur l'adresse IP du routeur. Effectuer la commande
                          "echo 1" puis retourner la sortie de cette commande vers le fichier
                          /proc/sys/net/ipv4/ip_forward
        '''     
        
        reponse = self.findInfoRouteur(nomFichier,nomRouteur)
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(reponse[1], username="root", password="vitrygtr")
        client.exec_command("echo 1 | sudo tee /proc/sys/net/ipv4/ip_forward")        
        
        
    def sshAddRoute(self,nomFichier,nomRouteur,destination,masque,via):
        '''
        Paramètres : 
            - nomFichier (String) : nom du fichier où les informations seront enregistrées
            - nomRouteur (String) : nom du routeur
            - destination (String) : destination de la route que l'on va créer
            - masque (String) : masque de la route que l'on va créer
            - via (String) : passerelle par défaut de la route que l'on va créer
            
        But : Fonction permettant de créer une route.
        
        Fonctionnement :  Effectuer une connexion en ssh sur l'adresse IP du routeur. Ajouter une route
                          grâce à la commande "route add"
        '''        
        
        reponse = self.findInfoRouteur(nomFichier,nomRouteur)
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(reponse[1], username="root", password="vitrygtr")
        client.exec_command("sudo route add -net "+destination+" netmask "+masque+" gw "+via)

    
    def sshDelRoute(self,nomFichier,nomRouteur,destination,masque,via):
        '''
        Paramètres : 
            - nomFichier (String) : nom du fichier où les informations seront enregistrées
            - nomRouteur (String) : nom du routeur
            - destination (String) : destination de la route que l'on va créer
            - masque (String) : masque de la route que l'on va créer
            - via (String) : passerelle par défaut de la route que l'on va créer
            
        But : Fonction permettant de supprimer une route.
        
        Fonctionnement :  Effectuer une connexion en ssh sur l'adresse IP du routeur. Supprimer une route
                          grâce à la commande "route del"
        '''          
        
        reponse = self.findInfoRouteur(nomFichier,nomRouteur)
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(reponse[1], username="root", password="vitrygtr")
        client.exec_command("sudo route del -net "+destination+" netmask "+masque+" gw "+via)
       