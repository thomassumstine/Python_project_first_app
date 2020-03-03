from django.db import models
from helpers import stringify_dict
# Create your models here.


class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 320)
    password = models.CharField(max_length = 60)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def full_name(self):
        return self.first_name + " " + self.last_name

    def __str__(self):
        return stringify_dict(self.__dict__)


class Wishes(models.Model):
    I_wish_for = models.CharField(max_length=255)
    wish_description = models.CharField(max_length=255)
    # 1 User to Many Wishes relationship
    # User will have a key called created_wishes
    created_by = models.ForeignKey(User, related_name="created_wishes")
    new_wish_field=models.BooleanField(default=False)
    # one many to many relationship
    # one user can like many wishes but one wish can be liked by many users
    likers = models.ManyToManyField(User, related_name="liked_wishes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return stringify_dict(self.__dict__)
