from django.contrib import admin

from catalog.models import Product, Category, PropertyObject, PropertyValue

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(PropertyObject)
admin.site.register(PropertyValue)