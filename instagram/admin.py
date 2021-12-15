from django.contrib import admin

# Register your models here.
from .models import Admin,Task,Chunk

admin.site.register(Admin)
admin.site.register(Task)
admin.site.register(Chunk)
