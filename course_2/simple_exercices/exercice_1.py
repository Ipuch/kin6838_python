"""
Mon premier exercice avec numpy
"""
import numpy as np

vecteur = np.array([12, 32, 5, 54, 64])

# Calculer la moyenne de a
moyenne_vecteur = np.mean(vecteur)    # à l'aide d'une fonction
moyenne_vecteur = vecteur.mean()      # à l'aide d'une méthode


print("Resultat:", moyenne_vecteur)


# Exercice 1
# Ecrire la mediane du vecteur avec à l'aide d'une fonction
# ...
np.median(vecteur)

# Exercice 2
matrice = np.array([[1,2],[3,4]])

print("Matrice", matrice)

moyenne_vertical = matrice.mean(axis=0)
moyenne_horizontal = matrice.mean(axis=1)
# Et en une seule ligne !
moyenne_combinee = matrice.mean(axis=1).mean(axis=0)

print("Moyennes", moyenne_vertical, moyenne_horizontal, moyenne_combinee)
# Ecrire la mediane de la moyenne des données verticale en une seule ligne de code
# ...