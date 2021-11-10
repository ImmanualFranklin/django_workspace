from django.contrib import admin

from userdata.models import UserDetail ,Team

# Register your models here.

admin.site.register(Team)
admin.site.register(UserDetail)