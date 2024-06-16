from django.contrib import admin
from music_streaming_app.models import *

# Register your models here.
class MusicAdmin(admin.ModelAdmin):
    pass

admin.site.register(User, MusicAdmin)
