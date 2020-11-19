from django.db import models
from django.conf import settings
from company.models import Company

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='user_company')
    position = models.CharField(max_length=40)
    phone_number = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f'Profile for the user {self.user.username}'

    @property
    def get_photo_url(self):
        if self.photo and hasattr(self.photo, 'url'):
            return self.photo.url
        else:
            return 'https://upload.wikimedia.org/wikipedia/commons/7/7c/Profile_avatar_placeholder_large.png'