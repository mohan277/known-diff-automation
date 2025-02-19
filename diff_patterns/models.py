from django.db import models

from account.models import Users


class KnownDiff(models.Model):
    diff_name = models.CharField(max_length=200)
    rule_id = models.CharField(max_length=10)
    description = models.JSONField(blank=True, null=True)
    diff_url = models.URLField(blank=True, null=True)
    diff_data = models.JSONField(blank=True, null=True)
    diff_image = models.URLField(blank=True, null=True)

    created_by = models.ForeignKey(
        Users, on_delete=models.CASCADE,
        blank=True, null=True, related_name="created_by"
    )
    raised_by = models.ForeignKey(
        Users, on_delete=models.CASCADE,
        blank=True, null=True, related_name="raised_by"
    )
    assigned_to = models.ForeignKey(
        Users, on_delete=models.CASCADE,
        blank=True, null=True, related_name="assigned_to"
    )
    approved_by = models.ForeignKey(
        Users, on_delete=models.CASCADE,
        blank=True, null=True, related_name="approved_by"
    )
    approved_at = models.DateTimeField(blank=True, null=True)

    is_active = models.IntegerField(
        default=0
    )  # 0. pending, 1. approved, 2. rejected, 3. deleted
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.diff_name

    class Meta:
        indexes = [
            models.Index(fields=["diff_name"], name="idx_diff_name")
        ]
        db_table = "known_diff"
        verbose_name_plural = "KnownDiffs"
        ordering = ['-updated_at']
