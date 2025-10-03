from django.db import models
from django.core.validators import MaxLengthValidator
from django.core.exceptions import ValidationError

# Create your models here.
class Conference(models.Model):#modifier le comportement de la classe
    conference_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=255)
    THEME=[
        ('AI','Computer science & AI'),
        ("SE","science & Engineering"),
        ("SS&E","Social science & Education"),
        ("I","Interdisciplinary")
    ]
    theme=models.CharField(max_length=255,choices=THEME)
    location=models.CharField(max_length=50)
    description=models.TextField(validators=[
        MaxLengthValidator(30,"la description ne doit pas dépasser 30 caractères")
    ])
    start_date=models.DateField()
    end_date=models.DateField()
    created_at=models.DateTimeField(auto_now_add=True)#avoir un historique dans la base de donnee
    updated_at=models.DateTimeField(auto_now=True)

    def clean(self):
        if self.start_date>self.end_date:
            raise ValidationError("la date de début doit être antérieur à la date de fin")

class Submission(models.Model):
    submission_id=models.CharField(max_length=8,primary_key=True,unique=True,editable=False )  
    title=models.CharField(max_length=255)
    abstract=models.TextField()
    keywords=models.TextField()
    paper=models.FileField(
        upload_to='papers/')#quand il ne trouve pas paper il va le créer
    STATUS=[
        ("Submitted", "Submitted"),
        ("Under Review", "Under Review"),
        ("Accepted", "Accepted"),
        ("Rejected", "Rejected"),
    ]
    status=models.CharField(max_length=255,choices=STATUS)
    submission_date=models.DateTimeField(auto_now_add=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    payed=models.BooleanField(default=False)
    user=models.ForeignKey("UserApp.User",
                           on_delete=models.CASCADE,
                           related_name="submissions")
    conference=models.ForeignKey(Conference,
                                 on_delete=models.CASCADE,
                                 related_name="submissions")


    




