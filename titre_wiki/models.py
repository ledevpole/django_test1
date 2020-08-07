from django.db import models

# Create your models here.

class Title(models.Model):
    title_wiki = models.CharField(max_length=200)
    article_id = models.IntegerField(default=0)

    def __str__(self):
        return self.title_wiki
