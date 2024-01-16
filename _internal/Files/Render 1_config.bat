@rem Enregistrer la clé publique dans la machine serveur (machine cible)

@rem Prérequis sur la machine cible :
@rem OpenSSH Serveur installé
@rem OpenSSH Serveur configuré en démarrage automatique et démarré
@rem Pas de parfeux bloquant les connexions entrantes sur le port 22
@rem Compte utilisateur non-admin
@rem Mot de passe de l'utilisateur connu (seule et unique fois où il sera nécessaire)


@rem Renseigner les données de la machine serveur (machine cible, compte non-admin)
@rem set domain=GEODEV-13
set name=backburner
set ip=192.168.0.50

scp "%userprofile%\.ssh\id_rsa.pub" "%name%@%ip%:C:\Users\%name%\.ssh\authorized_keys"

@rem pause

@rem Connexion test
@rem Tapper exit pour finir
@rem ssh "%name%"@%ip%

@rem pause
exit