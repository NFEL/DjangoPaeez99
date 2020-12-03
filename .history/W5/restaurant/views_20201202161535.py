from django.shortcuts import render, get_object_or_404
import folium

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
    location = ElementAddress.objects.get(element=element)

    locations = []
    for loc in ElementAddress.objects.filter(element=element):
        tmp = {}
        tmp['city'] = loc.city
        tmp['state'] = loc.state

        tmp['more'] = geolocator.reverse(loc.location)
        map = folium.Map(location=loc.location,zoom_start=20)
        folium.vector_layers.Circle(location=loc.location,radius=service_radius).add_to(map)
        folium.folium.vector_layers.path_options().add_to(map)
        tmp['map'] = map._repr_html_()
        locations.append(tmp)

    form = NearByReastaurantsForm(request.POST or None)
    if form.is_valid():
        f = form.save(commit=False)
        
    # elements = Element.objects.filter(category=category_obj)


    context = {
        'element': element,
        'locations': locations,
        'form' : form,
    }

    return render(request, 'element-detail.html', context)
