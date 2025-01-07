from django.contrib import admin
from .models import Ad

@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'price', 'location', 'is_sponsored', 'created_at']
    list_filter = ['is_sponsored', 'created_at']
    search_fields = ['title', 'description', 'user__username']
    list_editable = ['is_sponsored']
    date_hierarchy = 'created_at'
