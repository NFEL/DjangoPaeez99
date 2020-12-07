from django.urls import path, include

from .views import element_list, element_detail,ElementDetail

urlpatterns = [
    path('element-list/<int:cat_id>/<str:cat_title>',
         element_list, name='element-list'),
    path('element-detail/<int:elem_id>/', element_detail, name='element-detail'),
    # path('element-detail/<int:pk>', ElementDetail.as_view(), name='element-detail'),
]
