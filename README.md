# Open-Classrooms-Projet-9_Loïc

Ce projet OpenClassrooms a été créé dans le cadre du 9ème projet de formation. Il s'agit d'une application permettant à une communauté d'utilisateurs de consulter ou de solliciter une critique de livres à la demande.

Actuellement voici les fonctionnalités du programme : 

1. Inscription et connexion

2. Affichage des tickets et critiques des utilisateurs suivis sur le flux

3. Affichage des tickets et critiques de l'utilisateur connecté

4. Possibilité de créer une critique et/ou un ticket

5. Possibilité de suivre d'autres utilisateurs

6. Affichage et gestion des tickets et critiques soumis par l'utilisateur

## Pré-requis 

* Python 3 installé ([Télécharger Python](https://www.python.org/downloads/))
* Git ([Télécharger Git](https://github.com/))

## Installation

Pour la suite des instructions je conseille aux utilisateurs de Windows d'utiliser ([gitbash](https://git-scm.com/downloads))

1. **Téléchargement du projet.**


    Depuis votre terminal, placez-vous à l'endroit souhaité:
    
    ```cd [chemin d'accès]```  
    
    Creer un nouveau dossier:
    
    ```mkdir [nom de votre dossier]```

    Copier le programme source:

    ```git clone https://github.com/Lockco/Open-Classrooms-Projet-9```
    
2. **Creer un environnement virtuel.**

    Depuis windows/mac/linux: ```python3 -m venv env``` ou ```py -m venv env```
    
3. **Activer l'environnement.**
    
    Depuis windows: ``` source env\Scripts\activate.bat``` si cette commande ne fonctionne pas essayer la commande suivante : ```source env\Scripts\activate```
    
    Depuis mac/linux: ```source env/bin/activate```

4. **Installer les paquets.**

    Attention : pour éviter de rencontrer des problème avec ```pip``` veillez à vérifier que PYTHONPATH soit correctement configurées : 
    ([PYTHONPATH](https://datatofish.com/add-python-to-windows-path/))
    
    L'installation des paquets se fait en exécutant la commande suivante : ```pip install -r requirements.txt```
    
5. **Lancement du programme**

    Pour le démarrage du programme dans votre terminal verifier que vous êtes dans le dossier 
    où le projet a été cloné avec la commande suivante

    Sous linux : ```ls``` 
    Sous windows : ```dir```
    
    
    puis lancer le serveur à l'aide de la commande suivante :

    ```python manage.py runserver```

## Utilisation de l'application

1. Se connecter ou s'inscrire en utilisant les liens fournis sur la page d'accueil. N'ayant pas de compte nous vous invitons à créer votre compte. Des utilisateurs sont présents dans la base pour que vous puissiez utiliser l'onglet "Abonnements" voici la liste des utilisateurs présents : Benjamin, Claire, Julien, Luc, Lolyta. 

2. Consultez les tickets et les critiques des utilisateurs que vous suivez sur votre flux.

3. Ajoutez des utilisateurs à votre liste de suivi en entrant simplement leur nom d'utilisateur dans la zone de texte dédiée qui est située dans l'onglet 'Abonnement'.

4. Consulter la page qui liste tous les utilisateurs que vous suivez, avec l'option de dépliage pour arrêter de suivre un utilisateur donné dans l'onglet 'Abonnement'.

5. Accéder à une page dédiée à vos propres soumissions, où vous pouvez voir, modifier ou supprimer vos tickets et critiques dans l'onglet 'Post'.

6. Pour demander une critique, vous pouvez créer un ticket en spécifiant un livre ou un article de littérature. Les utilisateurs que vous suivez peuvent alors soumettre leurs critiques en réponse à ce ticket.

7. Vous pouvez également publier des critiques pour des livres et des articles sans ticket associé.

## Logiciel utilisé
[PyCharm] (https://www.jetbrains.com/fr-fr/pycharm/)

[Visual Studio Code] (https://code.visualstudio.com/download)

[gitbash] (https://git-scm.com/downloads)

## Remerciements

Merci à **Julien** et **Benjamin** pour leur aide précieuse.
