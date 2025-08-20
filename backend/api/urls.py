from django.urls import path
from .views import ListCreateModelSetView, RetrieveUpdateDestroyModelSetView, ListCreateUnitModelView, RetrieveUpdateDestroyUnitModelView

urlpatterns = [
    path('sets/', ListCreateModelSetView.as_view(), name='sets-list'),
    path('sets/<int:set_id>/', RetrieveUpdateDestroyModelSetView.as_view(), name='sets-detail'),

    path('sets/<int:set_id>/units/', ListCreateUnitModelView.as_view(), name='unit-list-create'),
    path('sets/<int:set_id>/units/<int:unit_id>/', RetrieveUpdateDestroyUnitModelView.as_view(), name='unit-update-destroy'),
]
