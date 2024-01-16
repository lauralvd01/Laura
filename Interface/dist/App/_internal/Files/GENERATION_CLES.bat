@rem Générer la paire de clés utilisateur pour la machine client (utilisateur lanceur de directives)
 
@rem Prérequis sur la machine client :
@rem OpenSSH Client installé (installé d'office sur Windows 10 et plus)
@rem OpenSSH Authentification Agent configuré en démarrage automatique et démarré
@rem Pas de parfeux bloquant les connexions sortantes sur le port 22

ssh-keygen
@rem Taper Entrée 3 fois de suite pour générer une clé RSA sans phrase secrète
@rem Résultat sur la machine client :
@rem Clé privée : "%userprofile%\.ssh\id_rsa"
@rem Clé publique : "%userprofile%\.ssh\id_rsa.pub"

pause

@rem Ajoute la clé privée à l'outil ssh-agent 
@echo off
net start ssh-agent
ssh-add "%userprofile%\.ssh\id_rsa"
@rem Supprime la clé privée de l'ordinateur (pour une meilleure sécurité, car elle n'est plus nécessaire une fois ajoutée au ssh-agent)
del "%userprofile%\.ssh\id_rsa"

pause
exit