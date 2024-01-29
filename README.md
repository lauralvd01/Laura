# Interface de commande de renders - Render control interface

## À destination des utilisateurs - For users
FR.

Téléchager le [Mode d'emploi](https://github.com/lauralvd01/Laura/blob/main/Mode%20d'emploi.pdf) et le dossier [App](https://github.com/lauralvd01/Laura/tree/main/App).
Lire et suivre les instructions du mode d'emploi.
Un fichier [config.csv](https://github.com/lauralvd01/Laura/blob/main/_internal/Files/config.csv) est disponible si besoin.

EN.

Download the [User manual](https://github.com/lauralvd01/Laura/blob/main/Mode%20d'emploi.pdf) (_Mode d'emploi_, written in French) and the [App](https://github.com/lauralvd01/Laura/tree/main/App) folder.
Read and follow the instructions in the manual.
A [config.csv](https://github.com/lauralvd01/Laura/blob/main/_internal/Files/config.csv) file is available if required.

## À destination des développeurs - For developpers
### Création de l'exéctuable - Application built
FR.

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

Si les modifications apportées au code ne nécessitent pas l'ajout de librairies (pas de _import_ ajouté) ou de fichiers autres (pas de dépendance ajoutée dans _App.spec_), alors il n'est pas nécessaire de redistribuer l'ensemble du dossier __App__ : seul l'exécutable est à remplacer.

EN.

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
