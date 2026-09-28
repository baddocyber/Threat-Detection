from django.db import models

# Create your models here.
from django.db import models

class ThreatLog(models.Model):

    timestamp = models.DateTimeField(auto_now_add=True)

    dur = models.FloatField()
    proto = models.CharField(max_length=50)
    service = models.CharField(max_length=50)
    state = models.CharField(max_length=50)

    Spkts = models.FloatField()
    Dpkts = models.FloatField()

    prediction = models.IntegerField()
    threat_level = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.threat_level} - {self.timestamp}"