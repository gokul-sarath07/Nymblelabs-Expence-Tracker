from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User


class Expense(models.Model):
    """This class creates the Expense model."""

    amount = models.PositiveIntegerField()
    date = models.DateField(default=now)
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    category = models.CharField(max_length=255)

    # Returns the string representation of this model.
    def __str__(self):
        return self.category


class Category(models.Model):
    """This class creates the Category model."""

    name = models.CharField(max_length=255)

    # returns the string representation of this model.
    def __str__(self):
        return self.name

    class Meta:
        """Meta class basically change the behavior of this model fields."""

        # The name that shows for this model in the django admin.
        verbose_name_plural = "Categories"
