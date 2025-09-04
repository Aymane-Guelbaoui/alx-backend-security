from django.db import models
from django.utils import timezone


class RequestLog(models.Model):
    ip_address = models.GenericIPAddressField()
    path = models.CharField(max_length=200)
    timestamp = models.DateTimeField(default=timezone.now)
    country = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.ip_address} at {self.path}"


class BlockedIP(models.Model):
    ip_address = models.GenericIPAddressField(unique=True)

    def __str__(self):
        return self.ip_address


class SuspiciousIP(models.Model):
    ip_address = models.GenericIPAddressField()
    reason = models.TextField()
    flagged_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.ip_address} - {self.reason}"
