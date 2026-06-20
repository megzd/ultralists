from django.db import models
from django.urls import reverse

# models are class blueprints that define empty tables
# migration files construct the tables from these blueprints
# an attribute in a model class represents a column in that table
# an object of a model class represents a row entry in that table

class List(models.Model):
    def get_absolute_url(self):
        return reverse("user_list", args=[self.id])


class Item(models.Model):
    # creates a new column with a default value of an empty string
    text = models.TextField(default="")
    # string references are best practice instead of passing the model class directly
    list = models.ForeignKey("List", default=None, on_delete=models.CASCADE)

    class Meta:
        ordering = ("id",)
        # each individual list should have unique to-do items
        unique_together = ("list", "text")
