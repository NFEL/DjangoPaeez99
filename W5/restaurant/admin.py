from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin

from . import models


admin.site.register(models.Element)
admin.site.register(models.ElementAddress,LeafletGeoAdmin)
admin.site.register(models.Category)
admin.site.register(models.SubCategory)
