from django.contrib import admin
from app.models import *
# Register your models here.


# class FileAdmin(admin.ModelAdmin):
#     list_display = ("name", "image")


admin.site.register(File)