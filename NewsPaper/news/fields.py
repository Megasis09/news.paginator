from django.db import models
from django.utils.translation import gettext_lazy as _

class UsernameField(models.CharField):
    def __init__(self, *args, **kwargs):
        super().__init__(
            max_length=150,
            unique=True,
            error_messages={
                'unique': _("A user with that username already exists."),
            },
            *args, **kwargs,
        )

    def db_type(self, connection):
        return 'varchar(150)'