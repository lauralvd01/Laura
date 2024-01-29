# Interface de commande de renders - Render control interface
![image](https://github.com/lauralvd01/Laura/assets/92759148/33f974a5-5bd7-472c-be62-b24e1d1c6a61)

<sup><sub>FR.</sub></sup>
<br />
__Application de contrôle à distance__, l'objectif étant de pouvoir redémarrer ou éteindre en une seule fois plusieurs ordinateurs connectés en réseau, depuis un seul poste adminsitrateur. 
Cela évite de se connecter à distance pour effectuer l'action souhaitée à la main sur chacun des ordinateurs (tests effectués sur un parc d'environ cinquante ordinateurs, nommés "renders" dans le [mode d'emploi](https://github.com/lauralvd01/Laura/blob/main/Mode%20d'emploi.pdf)). <br />
Technologie utilisée : connexion sécurisée par clé ssh avec l'outil OpenSSH de Windows 10. <br /> <br />

<sup><sub>EN.</sub></sup> 
<br />
__Remote control application__, the aim being to be able to reboot or shut down several networked computers at once, from a single administrator workstation. 
This eliminates the need to connect remotely to each computer to carry out the desired action manually (tests carried out on a fleet of around fifty computers, referred to as "renders" in the [user manual](https://github.com/lauralvd01/Laura/blob/main/Mode%20d'emploi.pdf)). <br />
Technology used : secure ssh-key connection using Windows 10's OpenSSH tool. <br /> <br />

## À destination des utilisateurs - For users
<sup><sub>FR.</sub></sup>
<br />
Téléchager le [Mode d'emploi](https://github.com/lauralvd01/Laura/blob/main/Mode%20d'emploi.pdf) et le dossier [App](https://github.com/lauralvd01/Laura/tree/main/App).
Lire et suivre les instructions du mode d'emploi. <br />
Un fichier [config.csv](https://github.com/lauralvd01/Laura/blob/main/_internal/Files/config.csv) est disponible si besoin. <br /> <br />

<sup><sub>EN.</sub></sup>
<br />
Download the [User manual](https://github.com/lauralvd01/Laura/blob/main/Mode%20d'emploi.pdf) (_Mode d'emploi_, written in French) and the [App](https://github.com/lauralvd01/Laura/tree/main/App) folder.
Read and follow the instructions in the manual. <br />
A [config.csv](https://github.com/lauralvd01/Laura/blob/main/_internal/Files/config.csv) file is available if required. <br /> <br />

## À destination des développeurs - For developpers
### Création de l'exéctuable - Application built
<sup><sub>FR.</sub></sup>
<br />
- Télécharger le repo et l'exporter.
- Télécharger Python (Python 3.11.6 utilisé pour l'ensemble de la création et production de l'application).
- Télécharger [Pyinstaller](https://pyinstaller.org/en/stable/) avec
```
pip install -U pyinstaller
```
- Dans le fichier _$path_to_the_Interface_folder$ \ App.spec_, modifier la ligne
```
datas=[('$path_to_the_ _internal_folder$\\Files\\arret_par_cle.bat', '.\\Files\\'),
('$path_to_the_ _internal_folder$\\Files\\connexion_par_cle.bat', '.\\Files\\'),
('$path_to_the_ _internal_folder$\\Files\\GENERATION_CLES.bat', '.\\Files\\'),
('$path_to_the_ _internal_folder$\\Files\\restart_par_cle.bat', '.\\Files\\'),
('$path_to_the_ _internal_folder$\\Files\\green.png', '.\\Files\\'),
('$path_to_the_ _internal_folder$\\Files\\red.png', '.\\Files\\')],
```
- Exécuter
```
pyinstaller $path_to_the_Interface_folder$\App.spec
```
- Récupérer le dossier __App__ contenant l'exécutable __App.exe__ ainsi que le dossier __internal__ contenant les librairies et le dossier __Files__ où sont et seront enregistrés les fichiers nécessaires / relatifs à l'application.

Si les modifications apportées au code ne nécessitent pas l'ajout de librairies (pas de _import_ ajouté) ou de fichiers autres (pas de dépendance ajoutée dans _App.spec_), alors il n'est pas nécessaire de redistribuer l'ensemble du dossier __App__ : seul l'exécutable est à remplacer. <br /> <br /> <br />

<sup><sub>EN.</sub></sup>
<br />
- Download the repo and export it.
- Download Python (Python 3.11.6 used for all application creation and production).
- Download Pyinstaller [Pyinstaller](https://pyinstaller.org/en/stable/) with
```
pip install -U pyinstaller
```
- In the file _$path_to_the_Interface_folder$ \ App.spec_, change the line
```
datas=[('$path_to_the_ _internal_folder$\\Files\\arret_par_cle.bat', '.\\Files\\'),
('$path_to_the_ _internal_folder$\\Files\\connexion_par_cle.bat', '.\\Files\\'),
('$path_to_the_ _internal_folder$\\Files\\GENERATION_CLES.bat', '.\\Files\\'),
('$path_to_the_ _internal_folder$\\Files\\restart_par_cle.bat', '.\\Files\\'),
('$path_to_the_ _internal_folder$\\Files\\green.png', '.\\Files\\'),
('$path_to_the_ _internal_folder$\\Files\\red.png', '.\\Files\\')],
```
- Run
```
pyinstaller $path_to_the_Interface_folder$\App.spec
```
- Retrieve the __App__ folder containing the __App.exe__ executable, as well as the __internal__ folder containing the libraries and the __Files__ folder where the necessary / related application files are and will be stored.

If the modifications made to the code do not require the addition of libraries (no _import_ added) or other files (no dependencies added in _App.spec_), then it is not necessary to redistribute the entire __App__ folder : only the executable needs to be replaced.
