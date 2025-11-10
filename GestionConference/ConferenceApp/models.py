from django.db import models
from django.core.validators import MaxLengthValidator,RegexValidator
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.utils import timezone
import uuid 

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

    def __str__(self):
        return f"la conference a comme titre {self.name}"

    def clean(self):
        if self.start_date and self.end_date:
            if self.start_date>self.end_date:
                raise ValidationError("la date de début doit être antérieur à la date de fin")

    conference_title_validator = RegexValidator(
    regex=r'^[A-Za-zÀ-ÿ\s]+$',
    message="Le titre de la conférence ne doit contenir que des lettres et des espaces."
)



pdf_validator = FileExtensionValidator(
    allowed_extensions=['pdf'],
    message="Seuls les fichiers PDF sont autorisés."
)

def validate_keywords(value):
     # Séparer les mots-clés par virgule et supprimer les espaces
    keywords = [kw.strip() for kw in value.split(',') if kw.strip()]
    if len(keywords) > 10:
        raise ValidationError("Vous ne pouvez pas saisir plus de 10 mots-clés.")

def generate_submission_id():
    return "USB-"+uuid.uuid4().hex[:8].upper()


class Submission(models.Model):
    submission_id=models.CharField(max_length=8,primary_key=True,unique=True,editable=False )  
    title=models.CharField(max_length=255)
    abstract=models.TextField()
    keywords=models.TextField(max_length=255,validators=[validate_keywords],help_text="Séparez les mots-clés par des virgules. Maximum 10 mots-clés."   )
    paper=models.FileField(
        upload_to='papers/',validators=[
            FileExtensionValidator(
    allowed_extensions=['pdf'],
    message="Seuls les fichiers PDF sont autorisés."
)
        ])#quand il ne trouve pas paper il va le créer
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

    def clean(self):
        
        #fonction keywords 
        """keyword_list=[ ]
        if self.keywords:
            for k in self.keywords.split(","):
                k=k.strip()
                if k:
                    keyword_list.append(k)"""
        # 1️⃣ Vérifier que la conférence est à venir
        if self.submission_date:  # Vérifie que la conférence a un champ de date
            if self.conference.start_date < timezone.now().date() and self.submission_date>self.conference.start_date:
                raise ValidationError({
                    'conference': "La soumission ne peut être faite que pour des conférences à venir."
                })

        # 2️⃣ Ne rien faire si aucun user n’est encore défini
        if not self.user_id:
         return    

        # 2️⃣ Limiter le nombre de soumissions par utilisateur et par jour
        today = timezone.now().date()

        existing_submissions = Submission.objects.filter(
            user=self.user,
            submission_date__date=today
        )
        if self.pk:
            existing_submissions = existing_submissions.exclude(pk=self.pk)

        if existing_submissions.count() >= 3:
            raise ValidationError(
                f"Vous avez déjà atteint le nombre maximal de 3 soumissions pour la date du {today}."
            )
    def save(self, *args, **kwargs): #*args is for a format of a tuple and **kwargs is  for a format of a dictionary
         if not self.submission_id:
            newid = generate_submission_id()
            while Submission.objects.filter(submission_id=newid).exists():#tantque que le newid existe dans la base de donnee on genere un autre
                newid = generate_submission_id()
            self.submission_id=newid
           
            super().save(*args,**kwargs)     
