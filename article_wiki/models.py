from django.db import models

# Create your models here.
class Article(models.Model):
    article_content = models.CharField(max_length=200)
    title_id = models.IntegerField(default=0)

    def __str__(self):
        return self.article_content
