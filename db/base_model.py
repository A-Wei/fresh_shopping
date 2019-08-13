from django.db import models


class BaseModel(models.Model):
    """Define an abustract Base Model
    Adds 3 files for all models
        created_at
        updated_at
        is_delete
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_delete = models.BooleanField(default=False)

    class Meta:
        abstract = True
