class Portefeuille:
    def __init__(self):
        self.pieces = 0
        self.billets = 0
        
    def ajouter_pieces(self, nombre):
        self.pieces += nombre
        
    def ajouter_billets(self, nombre):
        self.billets += nombre
        
    def compter_pieces(self):
        return self.pieces
    
    def compter_billets(self):
        return self.billets
    
    def valeur_totale(self):
        return self.pieces + self.billets * 10
    
    

# Exemple:
mon_portefeuille = Portefeuille()


# BOUCLE FOR
# Ajouter des pièces jusqu'à 5
for i in range(5):
    mon_portefeuille.ajouter_pieces(1)
    
print("Argent totale:", mon_portefeuille.valeur_totale())


# CONDITION IF
# ajouter de l'argent
argent_supplementaire = 11

if argent_supplementaire > 10:
    # si supérieur à 10 je préfère ajouter des billets
    mon_portefeuille.ajouter_billets(argent_supplementaire // 10)
    mon_portefeuille.ajouter_pieces(argent_supplementaire % 10)
    
else:
    # sinon ajoute des pièces.
    mon_portefeuille.ajouter_pieces(argent_supplementaire)
    
print("Argent totale:", mon_portefeuille.valeur_totale())
    

# BOUCLE WHILE
# ajouter des pièces jusqu'à 200
while mon_portefeuille.valeur_totale() < 200:
    mon_portefeuille.ajouter_pieces(1)
    
print("Argent totale:", mon_portefeuille.valeur_totale())


# Exercice 
# proposer une boucle while qui ajoute des billets 
# si la difference entre le montant à atteindre le montant courant 
# est supérieur à 10


    