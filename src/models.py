from django.db import models
from django.contrib.auth.models import User

class Book (models.Model):
    title = models.CharField(max_length=100, null=False, blank=False)
    author = models.CharField(max_length=50, null=False, blank=False)
    date_of_public = models.DateField(null=False, blank=False)
    isbn = models.IntegerField(null=True, blank=True)
    page_count = models.IntegerField(null=False, blank=False)
    cover_link = models.URLField(null=False, blank=False)
    lang = models.CharField(max_length=20, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='book', null=True, blank=True)
