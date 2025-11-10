from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError 
#from ConferenceApp.models import Conference


room_validator=RegexValidator(
    regex=r'^[a-zA-Z0-9\s-]+$',
    message='le nom doit contenir uniquement des lettres et des chiffres'   
)
# Create your models here.
class Session(models.Model):
    session_id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=255)
    topic=models.CharField(max_length=255)
    session_day=models.DateField()
    start_time=models.TimeField()
    end_time=models.TimeField()
    room=models.CharField(max_length=255,validators=[room_validator])
    conference=models.ForeignKey("ConferenceApp.Conference",
                                 on_delete=models.CASCADE,
                                 related_name="sessions")
    #conference=models.ForeignKey(Conference,on_delete=models.CASCADE,related_name="sessions")#cascade:pour eviter les problemes de suppression d'un attribut(fk) ds la base de donnée (lié au table mère:conference)
    created_at=models.DateTimeField(auto_now_add=True)#avoir un historique dans la base de donnee
    updated_at=models.DateTimeField(auto_now=True)

    def clean(self):
        
        if self.start_time and self.end_time:
            if self.start_time >= self.end_time:
                raise ValidationError("L'heure de fin doit être supérieure à l'heure de début.")
        
    
        if self.conference and self.session_day:
            if not (self.conference.start_date <= self.session_day <= self.conference.end_date):
                raise ValidationError("La date de la session doit être comprise entre le début et la fin de la conférence.")

    def __str__(self):
        return self.title#pourquoi on l'écrit ici?  #afficher le nom de la session dans l'admin 