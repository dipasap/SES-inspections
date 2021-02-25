from django.db import models
from django.contrib.auth.models import AbstractUser
from easy_thumbnails.files import get_thumbnailer
# Create your models here.


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField('email address', unique=True)
    phone_number = models.CharField(max_length=50, null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile_image/', null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    is_inspector = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return "- %s" %(self.get_full_name())

    def get_thumbnail(self):
        options = {'size': (300, 300), 'crop':'smart'}
        return get_thumbnailer(self.profile_image).get_thumbnail(options).url

    def get_image(self):
        if self.profile_image:
            try:
                return "<img class='table-avatar' src='%s'/>"%self.get_thumbnail()
            except:
                return "<img class='table-avatar' src='%s'/>"%self.profile_image.url
        return ""
