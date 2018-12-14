# tpArchiDistrib

J'ai gardé le code initial avec un RabbitMq que je fais tourner en local ainsi que le filesystem local
pour pouvoir me concentrer sur l'intégration d'un composant noSQL externe

Pour ce TP j'ai choisi d'utiliser dynamodb, la solution d'AWS, car celle ci remplit les conditions nécessaires
à l'enregistrement des tuples (uuid, source,target,status) et que je possédais les accès sur la plateforme aws (et non google pub sub)