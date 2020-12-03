from django.shortcuts import render, get_object_or_404
import folium

from geolocation import geolocator

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
    location = ElementAddress.objects.get(element=element)

    locations = []
    for loc in ElementAddress.objects.get(element=element):
        tmp = []
        tmp.append(loc.city)
        tmp.append(loc.state)
        tmp.append(geolocator.geocode(location.location))
        map = folium.Map(location=location.location)
        folium.Marker(location=location.location).add_to(map)
        tmp.append(map._repr_html_())

    context = {
        'element': element,
        'locations': locations,
    }

    return render(request, 'element-detail.html', context)
