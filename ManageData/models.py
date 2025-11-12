from django.db import models
from django.db.models import CharField, TextField


# Create your models here.
class StoreModel(models.Model):
    UUID = CharField(max_length=255, blank=True, primary_key=True)
    Name = CharField(max_length=255, null=True)
    Description = TextField(null=True)
    Address = CharField(max_length=255, null=True)
    Items = TextField(null=True)
    #Maybe add an image for stores

    class Meta:
        db_table = 'stores'