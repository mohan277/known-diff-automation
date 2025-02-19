from django.contrib import admin
from diff_patterns.models import KnownDiff


@admin.register(KnownDiff)
class KnownDiffInfo(admin.ModelAdmin):
    list_display = ['id', 'diff_name', 'rule_id', 'is_active', 'created_at', 'updated_at']
    search_fields = ['id', 'diff_name']
    list_filter = ['is_active']

    def get_ordering(self, request):
        return ['-created_at']
