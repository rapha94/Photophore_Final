Photophore

Projet de fin d'?tude ESME Sudria
Adrien BAUDE
Raphael Presberg


Protocole d'installation

-> Cloner le repository
-> Avoir python3
-> Se placer dans le dossier du projet
-> pip3 install -r requirements.txt
-> T?l?charger le fichier vgg16.h5 avec ce lien : https://drive.google.com/open?id=1jcPHCuBIMVppU6Y9advt1Cjc6Bn8AdA1
-> Placer le fichier dans /Scripts/VGG16
-> python3 /Scripts/db.py


Execution

-> Se placer dans le dossier
-> python3 main.py


Reset database

-> Supprimer le fichier database.db
-> Se placer dans le dossier du projet
-> python3 /Scripts/db.py


Visualiser Doc

-> Lancer index.html dans le dossier html


Reg?n?rer Doc

-> Supprimer dossier html
-> doxygen config.dox
