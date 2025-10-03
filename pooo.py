class  Vehicule:
    def __init__(self ,marque , annee, kilometrage, numero_serie):
        self._marque=marque #attribut protectetd
        self.__annee=annee #attribut private
        self.kilometrage=kilometrage
        self.numero_serie=numero_serie
    #setters
    @property
    def annee(self):
        return self.__annee 
    #setters
    @annee.setter
    def annee(self, nouvel_val):
        self.__annee=nouvel_val 

    def __str__(self):
        return f"les information de vehicule sont: marque: {self._marque}, annee: {self.annee}, kilometrage: {self.kilometrage}, numero_serie: {self.numero_serie}"
    
class Voiture(Vehicule): #class fille
    def __init__(self, marque, annee, kilometrage, numero_serie, color,prix):#constructeur pour l'initiation
        super().__init__(marque, annee, kilometrage, numero_serie)
        self.color = color
        self.prix = prix

    def __str__(self):
        return f"les information de voitures sont:  color: {self.color}, prix: {self.prix}"





v=Vehicule("Toyota", 2023, 20000, "123ABC")

voiture=Voiture("Honda", 2022, 15000, "456DEF", "Rouge", 20000)
print(voiture.__class__) #afficher le clasee de l'instance voiture

print(voiture)
print(v)
print (v.__dict__) #affiche les attributs de l'objet
v.annee=20
print (v._marque)
print (v._Vehicule__annee) #pour acceder a un attribut private
