from django.db import models

from categories.models import Category
from users.models import User


class Advertisement(models.Model):
    name = models.CharField(max_length=150, null=True, blank=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.IntegerField(null=True, blank=False)
    description = models.CharField(max_length=3000, null=True, blank=True)
    is_published = models.BooleanField(default=False)
    image = models.ImageField(upload_to='images/')
    category_id = models.ForeignKey(Category, on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'


