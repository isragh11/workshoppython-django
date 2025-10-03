class Vehicule:
    def __init__(self,marque,annee,kilometrage,numero_serie):
        self.marque = marque
        self.annee = annee
        self.kilometrage = kilometrage
        self.numero_serie = numero_serie
    def __str__(self):
        return f"les informations du Vehicule: {self.marque}, Année: {self.annee}"    

v=Vehicule("Toyota",2023,20000,"123ABC")
print(v)
