from django.db import models
from django.contrib.auth.models import AbstractUser
from db.base_model import BaseModel

# Create your models here.
class User(AbstractUser, BaseModel):
    """User Models
    AbstrictUser model from Django freamwork will craete email/password fields automaticly
    """

    class Meta:
        db_table = "fs_user"


class Address(BaseModel):
    user = models.ForeignKey("User", on_delete=True)
    receiver = models.CharField(max_length=20)
    addr = models.CharField(max_length=120)
    zip_code = models.CharField(max_length=6, null=True)
    phone = models.CharField(max_length=11)
    is_default = models.BooleanField(default=False)

    class Meta:
        db_table = "fs_address"
