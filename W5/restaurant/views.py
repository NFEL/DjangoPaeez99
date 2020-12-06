from django.http.response import JsonResponse
from django.shortcuts import render, get_object_or_404
# from django.contrib.gis.geos import GEOSGeometry
from django.http import HttpResponseRedirect
import folium
from folium.vector_layers import path_options

from geolocation import geolocator

from .models import Category, Element, ElementAddress

from .forms import MarketEntryForm

def element_list(request, cat_id, cat_title):
    category_obj = get_object_or_404(Category, id=cat_id)
    print(cat_title)
    elements = category_obj.element_set.all()
    
    context = {
        'category': category_obj,
        'elements': elements,
    }
    return render(request, 'element-list.html', context)


def element_detail(request, elem_id, service_radius):
    
    element = get_object_or_404(Element, id=elem_id)
    # location = ElementAddress.objects.get(element=element)

    locations = []
    for loc in ElementAddress.objects.filter(element=element):
        tmp = {}
        tmp['city'] = loc.city
        tmp['state'] = loc.state

        try :
            tmp['more'] = geolocator.reverse(loc.location)
        except Exception:
            pass
        map = folium.Map(location=loc.location,zoom_start=20)
        folium.vector_layers.Circle(loc.location,service_radius,fill=True).add_to(map)
        folium.vector_layers.Marker(loc.location).add_to(map)
        



        tmp['map'] = map._repr_html_()
        locations.append(tmp)

    form = MarketEntryForm(request.POST or None)
    if form.is_valid():
        f = form.save(commit=False)
        
    # elements = Element.objects.filter(category=category_obj)

    if request.method == 'POST':
        
        form = MarketEntryForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            user_location = form.cleaned_data.get('point')
            print(form.cleaned_data.get('point'))

            disctance = locations.distance()



    context = {
        'map' : map._repr_html_(),
        'element': element,
        'locations': locations,
        'form' : form,
    }

    return render(request, 'element-detail.html', context)
