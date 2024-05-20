from apps.user.utils.email import generate_verify_code, send_verify_email
from application.settings import TABLE_PREFIX, EMAIL_VALIDATION_TIME_LIMIT
from django.apps import apps
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.validators import validate_email
from django.core.exceptions import ValidationError as ValitonError
from datetime import timedelta


# EMAIL RELATED MODELS


class EmailSuffixFormat(models.Model):
    format = models.CharField(
        _("email format"), max_length=255, unique=True, primary_key=True
    )

    class Meta:
        db_table = TABLE_PREFIX + "email_format"

    def __str__(self):
        return self.format


class EmailTag(models.Model):
    tag = models.CharField(
        _("email tag"), max_length=255, unique=True, primary_key=True
    )

    class Meta:
        db_table = TABLE_PREFIX + "email_tag"

    def __str__(self):
        return self.tag


class EmailFormatTag(models.Model):
    email_format = models.ForeignKey(EmailSuffixFormat, on_delete=models.CASCADE)
    email_tag = models.ForeignKey(EmailTag, on_delete=models.CASCADE)

    class Meta:
        db_table = TABLE_PREFIX + "email_format_tag"
        unique_together = ("email_format", "email_tag")

    def __str__(self):
        return f"{self.email_format.format} - {self.email_tag.tag}"


# VALIDATOR


def check_email_suffix_format(value):
    message = "Please provide a valid email, check valid email format"
    code = "invalid_email_suffix_format"
    try:
        validate_email(value)
    except ValitonError as e:
        raise ValitonError(message, code=code, params={"value": value})

    _, suffix = value.rsplit("@", 1)

    try:
        suffix_formats = EmailSuffixFormat.objects.all()
    except EmailSuffixFormat.DoesNotExist:
        raise ValitonError(message, code=code, params={"value": value})
    for suffix_format in suffix_formats:
        if suffix_format.format == "@*" or suffix.startswith(suffix_format.format[1:]):
            return
    raise ValitonError(message, code=code, params={"value": value})


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
        check_email_suffix_format(email)
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

    def create_user(self, username, email=None, password=None, **extra_fields):
        role = Role.objects.get(role=ROLE_USER)
        return self._create_user(username, email, password, role)

    def create_admin(self, username, email=None, password=None, **extra_fields):
        role = Role.objects.get(role=ROLE_ADMIN)
        return self._create_user(username, email, password, role)

    def create_super_admin(self, username, email, password=None, **extra_fields):
        role = Role.objects.get(role=ROLE_SUPER_ADMIN)
        return self._create_user(username, email, password, role)


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # init email suffix format

    class Meta:
        abstract = True


class User(AbstractBaseUser, BaseModel):
    email = models.EmailField(
        _("email"),
        unique=True,
        db_index=True,
        primary_key=True,
        validators=[check_email_suffix_format],
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
        check_email_suffix_format(self.email)

    def upgrade_to_admin(self):
        self.role = Role.objects.get(role=ROLE_ADMIN)
        self.save(update_fields=["role"])

    def downgrade_to_user(self):
        self.role = Role.objects.get(role=ROLE_USER)
        self.save(update_fields=["role"])


class WaitingList(models.Model):
    email = models.EmailField(_("email"), unique=True, db_index=True, primary_key=True)
    username = models.CharField(_("username"), max_length=24, blank=False, null=False)
    password = models.CharField(_("password"), max_length=128, blank=False, null=False)
    verify_code = models.CharField(
        _("verify code"), max_length=6, blank=True, null=True
    )  # use update_time to check the expiration
    is_verified = models.BooleanField(_("is verified"), default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField(_("expired at"))

    class Meta:
        db_table = TABLE_PREFIX + "waiting_list"

    def __str__(self):
        return f"{self.username} ({self.email})"

    def plain_save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def update_verify_code(self):
        self.verify_code = generate_verify_code()
        self.expired_at = timezone.now() + timedelta(
            minutes=EMAIL_VALIDATION_TIME_LIMIT
        )
        send_verify_email(self.email, self.username, self.verify_code)
