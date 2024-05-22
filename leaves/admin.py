from django.contrib import admin
from .models import Leaves
# Register your models here.

@admin.register(Leaves)
class AuthorAdmin(admin.ModelAdmin):
    pass