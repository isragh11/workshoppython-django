from django.db import models
#from ConferenceApp.models import Conference

# Create your models here.
class Session(models.Model):
    session_id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=255)
    topic=models.CharField(max_length=255)
    session_day=models.DateField()
    start_time=models.TimeField()
    end_time=models.TimeField()
    room=models.CharField(max_length=255)
    conference=models.ForeignKey("ConferenceApp.Conference",
                                 on_delete=models.CASCADE,
                                 related_name="sessions")
    #conference=models.ForeignKey(Conference,on_delete=models.CASCADE,related_name="sessions")#cascade:pour eviter les problemes de suppression d'un attribut(fk) ds la base de donnée (lié au table mère:conference)
    created_at=models.DateTimeField(auto_now_add=True)#avoir un historique dans la base de donnee
    updated_at=models.DateTimeField(auto_now=True)
