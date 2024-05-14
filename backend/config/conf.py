# DATABASE SETTINGS

# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'HotSpotAnalyzerDB',
        'USER': 'root', # Change to your MySQL username
        'PASSWORD': "yourpassword", # Change to your MySQL password
        'HOST': 'localhost', # Change to your MySQL host
        'PORT': '3306', 
    }
}

# database table prefix
TABLE_PREFIX = "hotspot_sys_"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["*"]