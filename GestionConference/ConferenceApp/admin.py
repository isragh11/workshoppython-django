from django.contrib import admin
from .models import Conference 
from .models import Submission

# Register your models here.
admin.site.site_title="Gestion des conférences 25/26"
admin.site.site_header="Gestion conférences"
admin.site.index_title="django App Conferences"
admin.site.register(Conference)
admin.site.register(Submission)