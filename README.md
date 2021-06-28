# kepy_api
## 1. Présentation
Ceci est l'API utilisée par le bot Discord Kepy.  
L'API en elle même représente une portion de l'infrastructure nécessaire au bon fonctionnement du bot, qui a aussi besoin d'une base de données et d'un système de queue.  
C'est pour cela que le projet inclut un fichier `docker-compose.yml` prêt à être utilisé avec PostgreSQL, Celery et Redis.  

## 2. Fonctionnalités

Ce projet est toujours en construction, et ses fonctionnalités s'enrichiront au fur et à mesure que les besoins du bot évolueront.  

## 3. Utilisation

Après avoir cloné le projet, copier et remplir le fichier `.env.sample` renommé en `.env`  
Le déploiement actuel utilise Traefik, mais l'utilisation d'un autre reverse-proxy tel que NGINX est envisageable.  
S'assurer que Traefik est lancé et correctement configuré.  
Il n'y a plus qu'à utiliser docker-compose avec : `docker-compose up`
