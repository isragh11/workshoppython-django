from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
import uuid

def generate_user_id():
    return "USER"+uuid.uuid4().hex[:4].upper()   

def verify_email(email):
    domaines=["esprit.tn","sesame.com","tekup.tn","central.net"]
    email_domaine=email.split("@")[1]
    if email_domaine not in domaines:
        raise ValidationError("l'email est invalide et doit appartenir à un domaine universitaire privé")
        
name_validator=RegexValidator(
    regex=r'^[a-zA-Z\s-]+$',
    message='le nom doit contenir uniquement des lettres'   
)

# Create your models here.
class User(AbstractUser):
    user_id=models.CharField(max_length=8,primary_key=True,unique=True,editable=False )
    first_name=models.CharField(max_length=255,validators=[name_validator])
    last_name=models.CharField(max_length=255,validators=[name_validator])
    Role=[
        ("participant","participant"),
        ("organizer","organizer"),
        ("membre","member commitee"),
        ("commitee","organizing commitee member")
    ]
    role=models.CharField(max_length=255,choices=Role,default="participant")
    affiliation=models.CharField(max_length=255)
    email=models.EmailField(unique=True,validators=[verify_email])
    nationality=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)#avoir un historique dans la base de donnee
    updated_at=models.DateTimeField(auto_now=True)
    def save(self,*args,**kwargs):#args:format tuple envoyer des arguments sans clés et kwargs:format dictionnaire (des args avec clés)
        if not self.user_id:
            newid=generate_user_id()
            while User.objects.filter(user_id=newid).exists():
                newid=generate_user_id()
                self.user_id=newid    
            super().save(*args,**kwargs)#appel de la méthode save de la classe parente

class OrganizingCommitte(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,
                                 related_name="OrganizingCommitte")
    conference=models.ForeignKey("ConferenceApp.Conference",
                                 on_delete=models.CASCADE,
                                 related_name="OrganizingCommitte")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    committe_role=models.CharField(max_length=255,choices=[
        ("chair","chair"),
        ("co-chair","co-chair"),
        ("member","member"),
    ])
    date_joined=models.DateField() #la date d'ajout dans le comité
    


