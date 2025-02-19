from django.contrib import admin
from account.models import Users


@admin.register(Users)
class UsersInfo(admin.ModelAdmin):
    list_display = ['id', 'username', 'email_id', 'phone_number', 'is_active', 'created_at', 'updated_at']
    search_fields = ['id', 'username', 'email_id', 'phone_number']
    list_filter = ['is_active']

    def get_ordering(self, request):
        return ['-created_at']
