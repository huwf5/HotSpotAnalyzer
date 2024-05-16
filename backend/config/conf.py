# DATABASE SETTINGS

# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "HotSpotAnalyzerDB",
        "USER": "root",  # Change to your MySQL username
        "PASSWORD": "yourpassword",  # Change to your MySQL password
        "HOST": "localhost",  # Change to your MySQL host
        "PORT": "3306",
    }
}

# database table prefix
TABLE_PREFIX = "hotspot_sys_"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["*"]

# EMAIL SETTINGS
EMAIL_VALIDATION_TIME_LIMIT = 5  # 5 minutes
EMAIL_HOST = "smtp.163.com"
EMAIL_PORT = 25
EMAIL_HOST_USER = "your_email@gmail.com"  # Change to your email
EMAIL_HOST_PASSWORD = "your_password"  # Change to your email password
EMAIL_WHITELIST = [
    "@example.com",
]
# EMAIL_WHITELIST = ['@*'] # if not specified, all emails are allowed, other regex aren't allowed

# SUPER ADMIN SETTINGS
SUPER_ADMIN_EMAIL = "admin@example.com"
SUPER_ADMIN_USERNAME = "super_admin"
SUPER_ADMIN_PASSWORD = "superadminpassword"
