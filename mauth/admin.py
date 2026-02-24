from django.contrib import admin
from .models import countries, industries, myprofile
# Register your models here.

admin.site.register(countries)
admin.site.register(industries)
admin.site.register(myprofile)
