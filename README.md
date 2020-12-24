# Approche de modélisation du feu de forêt

### How to setup :
##### 1 : install dependencies
> pip install -r requirement.txt
##### 2 : Launch main.py 
> python main.py

### Présentation de cette solution au sujet des feux de forêt
Basée sur les systèmes multi agents, et notamment sur les automates cellulaires.
Plusieurs simulations avec des conditions initiales différentes ont été ajoutées pour mettre en évidence l'importance du seuil de percolation et permettre l'étude des hyperparamètres (probabilités de transition entre états):
* hyperparameters_gridsearch_percolation_threshold.csv et 
* simulation_ac_feu.json 
sont disponibles pour regarder les résultats, avec un script results.py

Les différents paramètres que vous pouvez régler sont :
##### Initialisation aléatoire des foyers
* area_block 		    	(int : côté du carré correspondant à chaque block de forêt)
* space_between_blocks 	    	(int : espace entre chaque block/forêt)
* percentage_apparition     	(int : [0;100] proba de faire apparaitre un block de forêt à l'initialisation)
##### Simulation
* percentage_alea_burning   	(int : [0;100] proba pour un arbre vert de bruler sans voisin en feu)
* percentage_neighbor_birth 	(int : [0;100] proba pour la naissance à un espace blanc d'un arbre vert si voisin vert)
* percentage_neighbor_burning  	(int : [0;100] proba pour un arbre vert de bruler avec voisin en feu)
##### Results study 
* percolation_threshold   	(int : [0;100] seuil pour lequel on affiche les hyperparametres permettant d'avoir une proportion de vert à long terme >percolation_threshold)

### Résumé global
Une grille 2D représente le monde. 
Chaque cellule du monde ne dispose que de 3 états possibles que l'on représente par des couleurs :
* Blanc : 0 = arbre brulé, mort -> Disparu 
* Vert  : 1 = arbre en bonne santé
* Rouge : 2 = arbre en feu

Les règles sont les suivantes, et chaque cellule évolue à chaque tour :
* SI Arbre en feu 	  (Rouge), ALORS Arbre disparu (Blanc)

* SI Arbre disparu  	  (Blanc), ALORS Arbre repousse (Vert) SI il a >=1 voisin vert ET (random <percentage_neighbor_birth % proba)
				   SINON Arbre disparu (Blanc)
* SI Arbre en bonne santé (Vert ), ALORS 
** SI >=1 voisin en feu	  (Rouge), ALORS Arbre en feu  (Rouge) (percentage_neighbor_burning % proba)
** SINON OU SI aucun voisin en feu        , ALORS Arbre en feu (percentage_alea_burning % proba)
** SINON Abre en bonne santé (Vert)
##### Seulement le voisinage de Von Neumann est considéré ici.