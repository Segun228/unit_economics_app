from django.urls import path
from .views import CacheView

urlpatterns = [
    path("", CacheView.as_view(), name = "check_cache_endpoint")
]