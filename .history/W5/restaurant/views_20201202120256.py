from django.shortcuts import render, get_object_or_404
import folium 
from geopy.geocoders import Nominatim 

from .models import Category, Element, ElementAddress


def element_list(request, cat_id, cat_title):
    category_obj = get_object_or_404(Category, id=cat_id)
    print(cat_title)
    elements = category_obj.element_set.all()
    # elements = Element.objects.filter(category=category_obj)

    context = {
        'category': category_obj,
        'elements': elements
    }
    return render(request, 'element-list.html', context)


def element_detail(request, elem_id):

    element = get_object_or_404(Element, id=elem_id)
    geolocator =Nominatim(user_agent='Mapsafood@gmail.com')
    location = ElementAddress.objects.get(element=element)
    location_geocoded = geolocator.geocode(location.location)
    folium.Map(location=location.location).save('/map.html')
    # elements = Element.objects.filter(category=category_obj)
    # addresses = element.address.all()
    context = {
        'element': element,
        'location' : location_geocoded,
        # 'addresses': addresses
    }
    return render(request, 'element-detail.html', context)
