class Portefeuille:
    def __init__(self):
        self.pieces = 0
        self.billets = 0
        
    def ajouter_pieces(self, nombre: int):
        self.pieces += nombre
        
    def ajouter_billets(self, nombre: int):
        self.billets += nombre
        
    def compter_pieces(self):
        return self.pieces
    
    def compter_billets(self):
        return self.billets
    
    def valeur_totale(self):
        return self.pieces + self.billets * 10
    
    def valeur_totale_billets(self):
        return  self.billets * 10 
    

# Exemple:

portefeuille__pierre = Portefeuille()

portefeuille__pierre.ajouter_pieces(1)
portefeuille__pierre.ajouter_pieces(2)
portefeuille__pierre.ajouter_billets(1)
portefeuille__pierre.ajouter_billets(2)

print(portefeuille__pierre.compter_pieces())  
print(portefeuille__pierre.compter_billets()) 
print(portefeuille__pierre.valeur_totale())

# Exercice ajouter une méthode qui compte la valeur des billets.
# ajouter une méthode qui compte l'argent des billets



