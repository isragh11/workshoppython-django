from django.contrib import admin
from .models import Conference 
from .models import Submission

# Register your models here.
admin.site.site_title="Gestion des conférences 25/26"
admin.site.site_header="Gestion conférences"
admin.site.index_title="django App Conferences"
#admin.site.register(Conference)#retourne la configuration par défaut
#admin.site.register(Submission)


#pour ajouter le formulaire de submission au formulaire de conference
class SubmissionInline(admin.TabularInline):#ou StackedInline
    model=Submission
    extra=1
    readonly_fields=["submission_date"]

@admin.register(Conference)#la meme chose que admin.site.register(Conference) mais ici je personnalise comme je veux
class AdminConferenceModel(admin.ModelAdmin):
    list_display=("name","theme","location","start_date","end_date","a")#tuple
    ordering=("start_date",)#trier par date croissante
    list_filter=("theme",)
    search_fields=("name","theme")#ajouter une barre de recherche
    date_hierarchy="start_date"#ajouter une hiérarchie par date
    fieldsets=(
        ("Informations general",{
            "fields":("conference_id","name","theme","description")
        }),
        ("Logistics Info",{
            "fields":("location","start_date","end_date")
        }),
    )
    readonly_fields=("conference_id",)
    def a(self,objet):
        if objet.start_date and objet.end_date:
            return (objet.end_date - objet.start_date).days
        return"RAS"#rien a signaler
    a.short_description="Duration (days)"#renommer le nom de la colonne duration

    inlines=[SubmissionInline]

    
@admin.action(description="marquer les soumissions comme payés")
def mark_as_payed(modeladmin,req,queryset):
    queryset.update(payed=True)
@admin.action
def mark_as_accepted(m,rq,q):
    q.update(status="accepted") 


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display =("title", "status", "payed","submission_date")
    fieldsets =(
        ("Information general", {
            "fields":("title","abstract","keywords")
        }),
        ("document", {
            "fields":("paper","user","conference")
        }),
        ("Status", {
            "fields":("status","payed")
        })
    )
    actions =[mark_as_payed,mark_as_accepted]