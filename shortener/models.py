from django.db import models
# Create your models here.
from django.db import models
from django.utils.timezone import now
from datetime import timedelta
def default_expiry():
    return now() + timedelta(hours=24)
class URL(models.Model):
    original_url = models.URLField(max_length=500)
    short_url = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(default=now)
    expires_at = models.DateTimeField(default=default_expiry)

    def __str__(self):
        return self.short_url

class Analytics(models.Model):
    short_url = models.ForeignKey(URL, on_delete=models.CASCADE)
    accessed_at = models.DateTimeField(default=now)
    ip_address = models.GenericIPAddressField()

    def __str__(self):
        return f"Analytics for {self.short_url.short_url}"
