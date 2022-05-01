from django.db import models
import uuid

class Address(models.Model):
   id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
   address = models.CharField(max_length=1000)
   lng = models.DecimalField(max_digits=10, decimal_places=7)
   lat = models.DecimalField(max_digits=10, decimal_places=7)
