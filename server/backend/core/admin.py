from django.contrib import admin
from .models import User, SessionCode

admin.site.register(User)
admin.site.register(SessionCode)
