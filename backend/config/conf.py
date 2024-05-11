# DATABASE SETTINGS

# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'HotSpotAnalyzerDB',
        # TODO: Change
        'USER': 'root', # Change to your MySQL username
        'PASSWORD': '123456', # Change to your MySQL password
        'HOST': 'localhost', # Change to your MySQL host
        'PORT': '3306', 
    }
}