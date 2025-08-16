from django.urls import path
from .views import ListCreateModeSetlView, RetrieveUpdateDestroyModelSetView, ListCreateUnitModelView, RetrieveUpdateDestroyUnitModelView

urlpatterns = [
    path('sets/<int:set_id>/units/', ListCreateUnitModelView.as_view(), name='post-list-create'),
    path('sets/<int:category_id>/units/<int:unit_id>/', RetrieveUpdateDestroyUnitModelView.as_view(), name='post-update-destroy'),

    path('sets/', ListCreateModeSetlView.as_view(), name='sets-list'),
    path('sets/<int:set_id>/', RetrieveUpdateDestroyModelSetView.as_view(), name='sets-detail'),

    path('units/', ListCreateUnitModelView.as_view(), name='units-list'),
    path('units/<int:unit_id>/', RetrieveUpdateDestroyUnitModelView.as_view(), name='units-detail'),
]
