from django.db import models


class Users(models.Model):
    username = models.CharField(max_length=50, blank=True, null=True)
    password = models.CharField(max_length=200, blank=True, null=True)
    email_id = models.EmailField(max_length=250, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["email_id"], name="idx_user_email_id")
        ]
        db_table = "users"
        verbose_name_plural = "Users"
