# from django.db import models
#
# # # Create your models here.
# # class Product(models.Model):
# #     name = models.CharField(max_length=100)
# #     price = models.IntegerField(default=0)   #cents
# #
# #
# #     def __str__(self):
# #         return self.name
# #     def get_display_price(self):
# #         return "{0:2f}".format(self.price/100)
# from django.db import models
#
# class Product(models.Model):
#     name = models.CharField(max_length=100)
#     price = models.IntegerField(default=0)  # cents
#     file = models.FileField(upload_to="product_files/", blank=True, null=True)
#     url = models.URLField(max_length=1000, default="http://example.com")
#
#     def __str__(self):
#         return self.name
#
#     def get_display_price(self):
#         return "{:.2f}".format(self.price / 100)


from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)  # cents
    file = models.FileField(upload_to="product_files/", blank=True, null=True)
    url = models.URLField()

    def __str__(self):
        return self.name

    def get_display_price(self):
        return "{0:.2f}".format(self.price / 100)