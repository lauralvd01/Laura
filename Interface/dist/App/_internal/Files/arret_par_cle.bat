@echo off

@rem À exécuter une fois que la connexion ssh par clé a été bien configurée

@rem Renseigner le nom du domaine, de l'utilisateur et de l'adresse ip de la machine cible
@rem set domain=GEODEV-13
set name=backburner
set ip=192.168.0.50

@rem Test connexion ssh vers la machine cible : décommenter
@rem Tapper exit pour continuer
@rem ssh %domain%\%name%@%ip%

@rem Connexion ssh vers la machine cible et exécution des commandes pour restart
ssh %name%@%ip% "taskkill /IM server.exe /F"
ssh %name%@%ip% "C:\Windows\System32\shutdown.exe -s -t 0"

exit