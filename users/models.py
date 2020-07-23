from django.db import models

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator

from core.models import AbstractBaseModel


class User(PermissionsMixin, AbstractBaseUser, AbstractBaseModel):
    """
    Table contains cognito-users & django-users.
    PermissionsMixin leverage built-in django model permissions system
    (which allows to limit information for staff users via Groups).
    Note: Django-admin user and app user not split in different tables because of simplicity of development.
    Some libraries assume there is only one user model, and they can't work with both.
    For example to have a history log of changes for entities - to save which user made a change of object attribute,
    perhaps, auth-related libs, and some other.
    With current implementation we don't need to fork, adapt and maintain third party packages.
    They should work out of the box.
    The disadvantage is - cognito-users will have unused fields which always empty. Not critical.
    """
    username_validator = UnicodeUsernameValidator()

    ### Common fields ###
    # For cognito-users username will contain `sub` claim from jwt token
    # (unique identifier (UUID) for the authenticated user).
    # For django-users it will contain username which will be used to login into django-admin site
    username = models.CharField('Username', max_length=255, unique=True, validators=[username_validator])
    is_active = models.BooleanField('Active', default=True)

    ### Cognito-user related fields ###
    # some additional fields which will be filled-out only for users registered via Cognito
    pass

    ### Django-user related fields ###
    # password is inherited from AbstractBaseUser
    email = models.EmailField('Email address', blank=True)  # allow non-unique emails
    is_staff = models.BooleanField(
        'staff status',
        default=False,
        help_text='Designates whether the user can log into this admin site.'
    )

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']  # used only on createsuperuser

    @property
    def is_django_user(self):
        return self.has_usable_password()