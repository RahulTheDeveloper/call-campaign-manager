from django.db import models
import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class User(AbstractUser):
    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("manager", "Manager"),
        ("agent", "Agent"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="agent")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]  # username is mandatory but login by email

    def __str__(self):
        return f"{self.email} ({self.role})"



class Agent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    agent_name = models.CharField(max_length=255)
    language = models.CharField(max_length=100, blank=True, null=True)
    voice_id = models.CharField(max_length=255, blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.agent_name


class Campaign(models.Model):
    CAMPAIGN_TYPE_CHOICES = (
        ("inbound", "Inbound"),
        ("outbound", "Outbound"),
    )

    CAMPAIGN_STATUS_CHOICES = (
        ("running", "Running"),
        ("paused", "Paused"),
        ("completed", "Completed"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    campaign_name = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=CAMPAIGN_TYPE_CHOICES)
    phone_number = models.CharField(max_length=30)
    status = models.CharField(max_length=20, choices=CAMPAIGN_STATUS_CHOICES, default="running")

    agents = models.ManyToManyField(Agent, related_name="campaigns")

    def __str__(self):
        return self.campaign_name


class CampaignResult(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    campaign = models.ForeignKey(Campaign, related_name='results', on_delete=models.CASCADE)

    name = models.CharField(max_length=255)              # Result name
    type = models.CharField(max_length=100)              # Type of result
    phone = models.CharField(max_length=30)
    cost = models.FloatField(default=0.0)
    outcome = models.CharField(max_length=100)
    call_duration = models.FloatField(default=0.0)
    recording = models.URLField(blank=True, null=True)   # URL of recording
    summary = models.TextField(blank=True, null=True)
    transcription = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.campaign.campaign_name} - {self.phone}"

