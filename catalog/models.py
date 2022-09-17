from django.db import models


class PropertyObject(models.Model):
    VALUE_TYPE_CHOICES = [
        ('int', 'integer'),
        ('str', 'string'),
    ]
    name = models.CharField(max_length=64)
    value_type = models.CharField(max_length=3, choices=VALUE_TYPE_CHOICES)
    code_url = models.CharField(max_length=64)

    class Meta:
        verbose_name = 'Характеристика'
        verbose_name_plural = 'Характеристики'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField()
    props = models.ManyToManyField(PropertyObject, blank=True, related_name='category_props')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=256)
    article = models.CharField(max_length=64)
    slug = models.SlugField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return str(self.id)


class PropertyValue(models.Model):
    str_val = models.CharField(max_length=128, null=True, blank=True)
    digit_val = models.FloatField(null=True, blank=True)
    code_url = models.CharField(max_length=64)
    prop = models.ForeignKey(PropertyObject, on_delete=models.CASCADE, related_name='prop_value')
    product = models.ManyToManyField(Product)

    def __str__(self):
        return str(self.id)












