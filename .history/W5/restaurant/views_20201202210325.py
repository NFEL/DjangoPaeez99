from django.shortcuts import render, get_object_or_404
import folium
from folium.vector_layers import path_options

from geolocation import geolocator

from .models import Category, Element, ElementAddress

from .forms import NearByReastaurantsForm

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
        folium.vector_layers.Circle(loc.location,service_radius,folium.vector_layers.path_options(fill=True)).add_to(map)
        folium.vector_layers.Marker(loc.location).add_to(map)
        
        print(folium.vector_layers.path_options(fill=True,fill_opacity=0.7))


        # lon =50.25
        # lat =-20.0

        # map_new = folium.map(location=(lon,lat),zoom_start=20)
        


        # folium.vector_layers.Marker(location=(51,-19.0215),path_options={
        #     'fill':'red',
        #     'stroke' : '5px',
        # }).add_to(map_new)
        
        # folium.vector_layers.Circle(location=(51,-19.0215),path_options={}).add_to(map_new)
        

        tmp['map'] = map._repr_html_()
        locations.append(tmp)

    form = NearByReastaurantsForm(request.POST or None)
    if form.is_valid():
        f = form.save(commit=False)
        
    # elements = Element.objects.filter(category=category_obj)


    context = {
        'map' : map._repr_html_(),
        'element': element,
        'locations': locations,
        'form' : form,
    }

    return render(request, 'element-detail.html', context)
