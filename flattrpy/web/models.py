
from datetime import datetime

from django.db import models

from django.contrib.auth.models import User


class APIToken(models.Model):
    """An OAuth token used to access the Flattr API.

    This maps from a token ID to its shared secret, and optionally the user
    on whose behalf we maintain it.  This helps minimize the amount of
    state we have to maintain during the OAuth dance.
    """
    id = models.CharField(max_length=50,primary_key=True)
    secret = models.CharField(max_length=50)
    user = models.ForeignKey(User,null=True,related_name="api_tokens")
    date_created = models.DateTimeField(null=True)

    def save(self,*args,**kwds):
        if not self.date_created:
            self.date_created = datetime.utcnow()
        return super(APIToken,self).save(*args,**kwds)


class Project(models.Model):
    """A Python Project; something that users might want to Flattr.

    Each project is identified by its top-level module name.  We maintain
    the project homepage URL and its flattr ThingID if known.
    """
    name = models.CharField(max_length=50,unique=True)
    homepage_url = models.CharField(max_length=300)
    thing_id = models.CharField(max_length=50)


