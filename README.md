# :notebook_with_decorative_cover: Projet Afpa Car
Site de covoiturage pour l'AFPA


Si parcel n'est pas installé sur la machine faire la commande "npm i -g parcel-bundler" <br>
Se mettre dans le dossier FrontEnd (la ou se trouve package.json)<br>
faire la commande "npm install"<br>
puis faire la commande "npm run start" ou "yarn start"<br>

Pour Linux il faut utiliser le fichier 'linux_requirements.txt'
<br>
Pour windows il faut utiliser le fichier 'requirements.txt'
<br>
### BDD
Un petite base de données est déjà présente sur la branche master :
On peut se connecter avec 'admin@admin.fr', les mots de passe de tous les utilisateurs crées sont 'afpa'
<br>
<br>

### PREREQUIS (temporaires)
Pour pouvoir créer les 'default trip' d'un utilisateur il doit avoir crée une adresse et il doit avoir un 'Centre AFPA' de sélectionné dans son profil
<br>
<br>

### WEBSOCKETS (disponible seulement sous linux, pour l'instant)

La partie 'chat' du site utilise des websockets et l'application django-channels. <br>
Il faut décommenter l'app 'channels' dans les 'INSTALLED_APPS' dans le settings.py
<br>
Il faut également install redis (installation sur une machine Ubuntu ci-dessous)

Dans un premier temps, il faut exécuter :
```
$ sudo apt update
$ sudo apt install redis-server
```

Ensuite on doit éditer ce fichier :
```
$ sudo nano /etc/redis/redis.conf
```
On cherche la ligne où il y a marqué 'supervised no' que l'on remplace par 'supervised systemd':
```
. . .

# If you run Redis from upstart or systemd, Redis can interact with your
# supervision tree. Options:
#   supervised no      - no supervision interaction
#   supervised upstart - signal upstart by putting Redis into SIGSTOP mode
#   supervised systemd - signal systemd by writing READY=1 to $NOTIFY_SOCKET
#   supervised auto    - detect upstart or systemd method based on
#                        UPSTART_JOB or NOTIFY_SOCKET environment variables
# Note: these supervision methods only signal "process is ready."
#       They do not enable continuous liveness pings back to your supervisor.
supervised systemd

. . .
```
On exécute ensuite :
```
$ sudo systemctl restart redis.service
```

Redis est normalement installé et configuré.
On va le tester :

```
$ sudo systemctl status redis
```

Si le serveur tourne on devrait avoir un message similaire à celui-ci :
```
● redis-server.service - Advanced key-value store
   Loaded: loaded (/lib/systemd/system/redis-server.service; enabled; vendor preset: enabled)
   Active: active (running) since Wed 2018-06-27 18:48:52 UTC; 12s ago
     Docs: http://redis.io/documentation,
           man:redis-server(1)
  Process: 2421 ExecStop=/bin/kill -s TERM $MAINPID (code=exited, status=0/SUCCESS)
  Process: 2424 ExecStart=/usr/bin/redis-server /etc/redis/redis.conf (code=exited, status=0/SUCCESS)
 Main PID: 2445 (redis-server)
    Tasks: 4 (limit: 4704)
   CGroup: /system.slice/redis-server.service
           └─2445 /usr/bin/redis-server 127.0.0.1:6379
. . .
```

Pour voir si redis fonctionne correctement :
```
$ redis-cli
```
Puis 'ping' la réponse de redis devrait être 'pong'
```
127.0.0.1:6379>Ping
```

Ensuite cette commande :
```
127.0.0.1:6379>set test "It's working!"
```
```
127.0.0.1:6379>get test
```
Si le message 'It's working' s'affiche c'est que ça fonctionne
Il faut tester si en redemarrant le message s'affiche toujours :
```
127.0.0.1:6379>exit
```
```
$ sudo systemctl restart redis
```
```
$ redis-cli
```
```
127.0.0.1:6379>get test
```
Si on a la réponse suivante c'est tout est bon :
```
"It's working!"
```

Tuto originel : https://www.digitalocean.com/community/tutorials/how-to-install-and-secure-redis-on-ubuntu-18-04
------------------------------------


Date | Version | Features
----| ----| ----
2018/07/31 | Version 0.1 | Users, Profil
2018/08/21 | Version 0.2 | New Users system
