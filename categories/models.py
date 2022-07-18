from django.db import models


class Category(models.Model):
    id = models.AutoField(editable=False, unique=True, primary_key=True, auto_created=True)
    name = models.CharField(max_length=50, null=True, blank=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
