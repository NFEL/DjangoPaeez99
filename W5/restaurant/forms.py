from django import forms
# from django.contrib.gis.db.models import fields
# from django.db.models import fields
from django.contrib.gis.geos import Point
from .models import ElementAddress

# class NearByReastaurantsForm(forms.ModelForm):
#     class Meta:
#         model = ElementAddress
#         fields = ('location',) 



class MarketEntryForm(forms.ModelForm):

    latitude = forms.FloatField(
        min_value=-90,
        max_value=90,
        required=True,
    )
    longitude = forms.FloatField(
        min_value=-180,
        max_value=180,
        required=True,
    )

    class Meta(object):
        model = ElementAddress
        fields = ('location',)
        widgets = {'point': forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        coordinates = self.initial.get('point', None)
        if isinstance(coordinates, Point):
            self.initial['longitude'], self.initial['latitude'] = coordinates.tuple

    def clean(self):
        data = super().clean()
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        point = data.get('point')
        if latitude and longitude and not point:
            data['point'] = Point(longitude, latitude)
        return data