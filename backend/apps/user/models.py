from django.db import models
from config.conf import TABLE_PREFIX

# Create your models here.


class Role(models.Model):
    ROLE_CHOICES = [
        ("Super Admin", "Super Admin"),
        ("Admin", "Admin"),
        ("User", "User"),
    ]
    role = models.CharField("Role", max_length=12, choices=ROLE_CHOICES)

    class Meta:
        db_table = TABLE_PREFIX + "role"

    def __str__(self):
        return self.role
