from apps.user.utils.email import (
    generate_verify_code,
    send_verify_email,
    EMAIL_USAGE_LIST,
    EMAIL_USAGE_FOR_REGISTER,
    EMAIL_USAGE_FOR_RESET_PASSWORD,
)
from django.core.exceptions import ValidationError
from application.settings import TABLE_PREFIX, EMAIL_VALIDATION_TIME_LIMIT
from django.apps import apps
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.validators import validate_email
from datetime import timedelta


# EMAIL RELATED MODELS


def validate_format(value):
    if not value.startswith("@"):
        raise ValidationError(_("The email format should start with '@'"))


class EmailSuffixFormat(models.Model):
    format = models.CharField(
        _("email format"),
        max_length=255,
        unique=True,
        primary_key=True,
        validators=[validate_format],
    )
    is_active = models.BooleanField(_("is active"), default=True)

    class Meta:
        db_table = TABLE_PREFIX + "email_format"
        app_label = 'user'  # 使用你的应用名称

    def __str__(self):
        return self.format

    def activate(self):
        self.is_active = True
        self.save(update_fields=["is_active"])

    def deactivate(self):
        self.is_active = False
        self.save(update_fields=["is_active"])


class EmailFormatTag(models.Model):
    email_format = models.ForeignKey(EmailSuffixFormat, on_delete=models.CASCADE)
    email_tag = models.CharField(_("email tag"), max_length=255)

    class Meta:
        db_table = TABLE_PREFIX + "email_format_tag"
        unique_together = ("email_format", "email_tag")

    def __str__(self):
        return f"{self.email_format.format} - {self.email_tag}"


# USER RELATED MODELS
ROLE_SUPER_ADMIN = "Super Admin"
ROLE_ADMIN = "Admin"
ROLE_USER = "User"

AdminList = [ROLE_SUPER_ADMIN, ROLE_ADMIN]


class Role(models.Model):
    ROLE_CHOICES = [
        (ROLE_SUPER_ADMIN, ROLE_SUPER_ADMIN),
        (ROLE_ADMIN, ROLE_ADMIN),
        (ROLE_USER, ROLE_USER),
    ]
    role = models.CharField("Role", max_length=12, choices=ROLE_CHOICES)

    class Meta:
        db_table = TABLE_PREFIX + "role"

    def __str__(self):
        return self.role


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, role):
        email = self.normalize_email(email)
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        username = GlobalUserModel.normalize_username(username)
        user = self.model(username=username, email=email, role=role)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user_from_waiting_list(self, waitinglist_user):
        role = Role.objects.get(role=ROLE_USER)
        user = self.model(
            username=waitinglist_user.username,
            email=waitinglist_user.email,
            password=waitinglist_user.password,  # Password is already hashed
            role=role,
        )
        user.save(using=self._db)
        return user

    def create_super_admin(self, username, email, password=None, **extra_fields):
        role = Role.objects.get(role=ROLE_SUPER_ADMIN)
        return self._create_user(username, email, password, role)


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # init email suffix format

    class Meta:
        abstract = True


class User(AbstractBaseUser, BaseModel, PermissionsMixin):
    email = models.EmailField(
        _("email"),
        unique=True,
        db_index=True,
        primary_key=True,
        validators=[validate_email],
    )
    username = models.CharField(_("username"), max_length=24)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    objects = UserManager()
    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "username",
    ]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        db_table = TABLE_PREFIX + "user"

    def __str__(self):
        return f"{self.username} ({self.email})"

    def clean(self) -> None:
        super().clean()

    def upgrade_to_admin(self):
        self.role = Role.objects.get(role=ROLE_ADMIN)
        self.save(update_fields=["role"])

    def downgrade_to_user(self):
        self.role = Role.objects.get(role=ROLE_USER)
        self.save(update_fields=["role"])

    @property
    def is_staff(self):
        return self.role.role in AdminList

    @property
    def is_active(self):
        return True

    @property
    def is_superuser(self):
        return self.role.role == ROLE_SUPER_ADMIN


EMAIL_USAGE_CHOICES = [
    (EMAIL_USAGE_FOR_REGISTER, EMAIL_USAGE_FOR_REGISTER),
    (EMAIL_USAGE_FOR_RESET_PASSWORD, EMAIL_USAGE_FOR_RESET_PASSWORD),
]


class EmailVerification(models.Model):
    email = models.EmailField(_("email"), db_index=True)
    verify_code = models.CharField(
        _("verify code"), max_length=6, blank=True, null=True
    )  # use update_time to check the expiration
    usage = models.CharField(
        _(f"usage: {EMAIL_USAGE_LIST}"), max_length=255, choices=EMAIL_USAGE_CHOICES
    )
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField(_("expired at"))

    class Meta:
        db_table = TABLE_PREFIX + "email_verification"
        unique_together = ("email", "usage")

    def __str__(self):
        return self.email

    def update_code(self):
        self.verify_code = generate_verify_code()
        self.expired_at = timezone.now() + timedelta(
            minutes=EMAIL_VALIDATION_TIME_LIMIT
        )
        send_verify_email(self.email, self.verify_code, usage=self.usage)

    def is_valid(self, code):
        return self.verify_code == code and self.expired_at > timezone.now()


class WaitingList(models.Model):
    email = models.EmailField(_("email"), unique=True, db_index=True, primary_key=True)
    username = models.CharField(_("username"), max_length=24, blank=False, null=False)
    password = models.CharField(_("password"), max_length=128, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = TABLE_PREFIX + "waiting_list"

    def __str__(self):
        return f"{self.username} ({self.email})"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def encrypt_password_and_save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super().save(*args, **kwargs)

    @classmethod
    def clean_by_email_suffix(cls, suffix):
        """Clean the waiting list by email suffix
        suffix: str, the suffix of the email, e.g. "@gmail.com", "@*"
        if suffix is "@*", then all the suffixes not in the active suffixes will be deleted

        """
        if suffix == "@*":
            active_suffixes = EmailSuffixFormat.objects.select_for_update().filter(
                is_active=True
            )
            if not active_suffixes:
                return
            regex_pattern = "|".join(
                [suffix.replace(".", r"\.") + "$" for suffix in active_suffixes]
            )
            emails_to_delete = cls.objects.select_for_update().exclude(email__regex=regex_pattern)
        else:
            print(suffix)
            emails_to_delete = cls.objects.select_for_update().filter(email__endswith=suffix)
            print(emails_to_delete)
        emails_to_delete.delete()
