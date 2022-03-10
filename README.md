# TurtleBot2_ROS2_foxy

## Attention à bien copier ce repo dans ~/dev_ws/src
Repository pour le cours de Rémi FABRE.

Ce projet porte sur le TurtleBot avec ROS2 et foxy.

Le but de ce projet est de réaliser un Follow_me mais aussi de réaliser un déplacement sur une carte cartographiée par le lidar du TurtleBot.

- à cloner dans ~/turtlebot3_ws/src
- ouvrir Gazebo et Rviz
- cd ~/turtlebot3_ws
- colcon build --symlink-install
- source ~/.bashrc
- ros2 run nav2_simple_commander working_on_foxy

mardi 10 mars :

- Récupération du code de M.FABRE qui a copié le dépot officiel : nav2_simple_commander/nav2_simple_commander/working_on_foxy.py
La seule modification de ce dépot est l'ajout de nav2_simple_commander/working_on_foxy.py (pour plus d'informations sur ce sujet lire le README.md sur le dépot de M.FABRE: https://bitbucket.org/RemiFabre/foxy_nav2_navigator/src/master/)
Compris dans cette récupération :

- launch/*
- media/*
- nav2_simple_commander/*
- resource/*
- setup.*
- test/*
- package.xml


Avec la collaboration de :

- Allan PIEDNOEL
- Florian TASSIS
- Anthony ORQUIN
- Charles STACCHINO