# TurtleBot2_ROS2_foxy

Repository pour le cours de Rémi FABRE.

Ce projet porte sur le TurtleBot avec ROS2 et foxy.

Le but de ce projet est de réaliser un __Follow me__ mais aussi de réaliser un déplacement sur une carte cartographiée par le lidar du TurtleBot.

L'épreuve se déroulera avec une carte préalablement cartographiée puis suivra ces étapes:

1- Le robot sera posée sur une position aléatoire dans la map 
2- Un bouton sera touché pour lancer le programme 
3- Le programme débutera par un follow_me
4- si la personne suivit ne bouge plus pendant 4/5secondes, le follow_me s'arrête 
5- le turtlebot devra retourné à sa position initiale.
6- Il devra ensuite aller à une position (x,y,theta) choisit par l'équipe

Pour se faire :

Nous allons utiliser une manette qui permet de contrôler le robot et qui sera le controller des actions demandées.
La manette permet de contrôler naturellement le turtlebot en x, y et theta.
Si l'on bouge le joystick droit cela permet d'activer :
- Dans un premier temps, recup_position pour récupérer la position initiale du robot
- Puis le follow_me. Ainsi la variable self.follow_me.active deviendra True. Cette dernière se modifiera si la personne arrêtera de bouger pendant 4/5s.
- Lorsque self.follow_me.active = False, cela lance la naviguation_goal avec les coordonnées récupérer dans la première étape.
- Puis après avoir atteint la position le robot ira à la position que nous aurons définie en (x,y,theta).
- Fin du programme -> on rend la main à la manette

voici une vidéo du résultat final : https://www.youtube.com/watch?v=ICJzIhcpE1s

---

## EXECUTION

Pour exécuter le programme en simulation:

- à cloner dans ~/turtlebot3_ws/src
- ouvrir Gazebo et Rviz
  - CTRL+ALT+T
  - export TURTLEBOT3_MODEL=burger
  - ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
  - CTRL+ALT+T
  - export TURTLEBOT3_MODEL=burger
  - ros2 launch turtlebot3_navigation2 navigation2.launch.py use_sim_time:=True map:=$HOME/map.yaml
- CTRL+ALT+T
- cd ~/turtlebot3_ws
- colcon build --symlink-install
- source ~/.bashrc
- ros2 run nav2_simple_commander main

Pour éxécuter le programme en réel:

- Avoir la même connexion internet sur l'ordinateur que sur le robot (nous avons utilisé un partage de connexion)
- CTRL+ALT+T 
- ssh ubuntu@192.168.90.244
- ros2 launch turtlebot3_bringup robot.launch.py
- CTRL+ALT+T
- cd ~/turtlebot3_ws
- colcon build --symlink-install
- source ~/.bashrc
- ros2 run nav2_simple_commander main

-----
## A QUOI SERVENT LES PROGRAMMES 

- main.py permet d'activer la communication entre le robot et la manette 
- controller.py permet de gérer les commandes de la manette, mais aussi d'activer le follow_me
- follow_me est appelé quand une variable activate=True, et permet aussi de lancer le navigation_goal.py
- navigation_goal(x,y,theta) permet d'aller à une position x,y,theta avec une carte préalablement cartographiée
- recup_position.py permet de récupérer la position en x,y,theta actuelle du robot


--------

Récupération du code de M.FABRE qui a copié le dépot officiel : nav2_simple_commander/nav2_simple_commander/working_on_foxy.py.

La seule modification de ce dépot est l'ajout de nav2_simple_commander/working_on_foxy.py (pour plus d'informations sur ce sujet lire le README.md sur le dépot de M.FABRE: https://bitbucket.org/RemiFabre/foxy_nav2_navigator/src/master/)
Compris dans cette récupération :

- launch/*
- media/*
- nav2_simple_commander/*
- resource/*
- setup.*
- test/*
- package.xml

------------------

Avec la collaboration de :

- Allan PIEDNOEL
- Florian TASSIS
- Anthony ORQUIN
- Charles STACCHINO