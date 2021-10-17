[![CI](https://github.com/SebGoliot/kepy_api/actions/workflows/main.yml/badge.svg)](https://github.com/SebGoliot/kepy_api/actions/workflows/main.yml)
[![codecov](https://codecov.io/gh/SebGoliot/kepy_api/branch/main/graph/badge.svg?token=I2CBHMQ04G)](https://codecov.io/gh/SebGoliot/kepy_api)

# kepy_api
## 1. Présentation
Ceci est l'API utilisée par le bot Discord [kepy](https://github.com/SebGoliot/kepy_bot).  
L'API en elle même représente une portion de l'infrastructure nécessaire au bon fonctionnement du bot, qui a aussi besoin d'une base de données et d'un système de queue.  
C'est pour cela que le projet inclut un fichier `docker-compose.yml` prêt à être utilisé avec PostgreSQL et Redis.  

## 2. Fonctionnalités

Ce projet est toujours en construction, et ses fonctionnalités s'enrichiront au fur et à mesure que les besoins du bot évolueront.  

## 3. Utilisation

Le déploiement actuel utilise Traefik, mais l'utilisation d'un autre reverse-proxy tel que NGINX est envisageable.  
Afin d'utiliser les interactions Discord, il est nécessaire de configurer un endpoint HTTP ainsi que des commandes auprès de l'API Discord.  

- Après avoir cloné le projet, copier et remplir le fichier `.env.sample` renommé en `.env`  
- S'assurer que Traefik est lancé et correctement configuré.  
- Il n'y a plus qu'à lancer docker-compose avec `docker-compose up`

