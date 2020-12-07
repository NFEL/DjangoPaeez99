from django.http.response import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.gis.geos import GEOSGeometry, Point
from django.http import HttpResponseRedirect, HttpResponseBadRequest
import folium
from folium.map import Tooltip
from folium.vector_layers import path_options
from django.views.generic import DetailView
from geopy import distance as dis
from ip2geotools.databases.noncommercial import DbIpCity

import urllib.request
import socket   

from geolocation import geolocator
from .models import Category, Element, ElementAddress
from .forms import UserLocationMarker



def element_list(request, cat_id, cat_title):
    category_obj = get_object_or_404(Category, id=cat_id)
    print(cat_title)
    elements = category_obj.element_set.all()

    context = {
        'category': category_obj,
        'elements': elements,
    }
    return render(request, 'element-list.html', context)


def element_detail(request, elem_id):


    element = get_object_or_404(Element, id=elem_id)

    locations = []
    

    form = UserLocationMarker(request.POST or None)
    if request.method == 'POST':
        user_location = None
        form = UserLocationMarker(request.POST)

        if form.is_valid():
            user_location = point_parser(request.POST.get('location' or None))

    elif request.method == 'GET':

        external_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')
        response = DbIpCity.get(external_ip , api_key='free')        
        user_location = (response.latitude,response.longitude)

        if form.is_valid():
            f = form.save(commit=False)
    else:
        return HttpResponseBadRequest()


    for loc in ElementAddress.objects.filter(element=element):

        tmp = {}
        tmp['city'] = loc.city
        tmp['state'] = loc.state
        location_corrected = (loc.location.y, loc.location.x)
        try:
            tmp['more'] = geolocator.reverse(location_corrected)
        except Exception:
            pass
        
        map = folium.Map(location=location_corrected,
                         zoom_start=10)
        folium.vector_layers.Circle(
            location_corrected,
            float(loc.service_radius),
            fill=True).add_to(map)
        folium.vector_layers.Marker(location_corrected).add_to(map)
        distance = dis.distance(
            user_location, Point(location_corrected)).km
        if distance < loc.service_radius/1000:
            flag_service = True
            status = 'You can order now'

        else:
            flag_service = False
            status = 'Boy you are far from here'

        if request.method == 'POST' :
            # folium.vector_layers.Marker(user_location,icon=folium.Icon(color='green',prefix='glyphicon',icon='home')).add_to(map)
            folium.vector_layers.PolyLine([user_location,location_corrected],popup='You to Restaurant',tooltip='You to Restaurant').add_to(map)
            tmp['distance'] = distance
            tmp['flag_service'] = flag_service
            tmp['status'] = status
        else:
            tmp['distance'] = None

        tmp['service_area'] =loc.service_radius
        tmp['map'] = map._repr_html_()
        locations.append(tmp)


    context = {
        'map': map._repr_html_(),
        'element': element,
        'locations': locations,
        'form': form,
        'user_location' : list(user_location),
    }

    return render(request, 'element-detail.html', context)


def point_parser(location):
    if isinstance(location, str):
        if location.__contains__('Point'):
            long = float(location.split('"coordinates":')[1].split(',')[0][1:])
            lat = float(location.split('"coordinates":')[1].split(',')[1][:-2])
            return Point((lat, long))


class ElementDetail(DetailView):
    model = Element
