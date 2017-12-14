Photophore

Projet de fin d'?tude ESME Sudria
Adrien BAUDE
Raphael Presberg


Protocole d'installation

-> Cloner le repository
-> Avoir python3
-> Se placer dans le dossier du projet
-> pip3 install -r requirements.txt
-> Telecharger le fichier vgg16_weights.h5 sur cette page https://gist.github.com/baraldilorenzo/07d7802847aaad0a35d3
-> Renommer le fichier en vgg16.h5 et le placer dans /Scripts/VGG16
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
