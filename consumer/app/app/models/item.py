from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator

class Item(models.Model):
    id = fields.IntField(pk=True)
    price = fields.CharField(max_length=20)
    volume = fields.CharField(max_length=20)
    funds = fields.CharField(max_length=20)
    market = fields.CharField(max_length=20)
    created_at = fields.CharField(max_length=30)

ItemIn = pydantic_model_creator(Item, name="ItemIn")
