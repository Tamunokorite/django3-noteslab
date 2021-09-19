from django.contrib import admin
from .models import Note

# Register your models here.
@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    readonly_fields = ['created', 'modified', 'deleted', 'date_deleted', 'user']