from django.db import models

# models are blueprints for creating empty tables
# migrations are the tables created from these blueprints
# an attribute in a model class represents a column in that table
# an object of a model class represents a row entry in that table

class List(models.Model):
    pass

class Item(models.Model):
    # creates a new column with a default value of an empty string
    text = models.TextField(default="")
    # string references are best practice instead of passing the model class directly
    list = models.ForeignKey("List", default=None, on_delete=models.CASCADE)
