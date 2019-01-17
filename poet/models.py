from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class PoetManager(BaseUserManager):
    def create_user(self, identifier, nickname, description=None, image=None, password=None):
        if not identifier or not nickname:
            raise ValueError("Nickname and identifier should not be empty")

        poet = self.model(
            identifier=identifier,
            nickname=nickname,
            image=image,
            description=description,
        )
        poet.set_password(password)
        poet.save(using=self._db)
        return poet

    def create_superuser(self, identifier, nickname, password):
        poet = self.create_user(
            identifier=identifier,
            nickname=nickname,
            password=password
        )
        poet.is_admin = True
        poet.save(using=self._db)
        return poet


class Poet(AbstractBaseUser):
    identifier = models.CharField('ID', max_length=30, unique=True)
    nickname = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=50, blank=True, null=True)
    image = models.ImageField(upload_to='user_image/', blank=True, null=True)
    joined_date = models.DateField(auto_now_add=True)
    recent_visited_date = models.DateTimeField(auto_now=True)
    do_get_email = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = PoetManager()
    USERNAME_FIELD = 'identifier'
    REQUIRED_FIELDS = ['nickname']

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    def __str__(self):
        return self.nickname
