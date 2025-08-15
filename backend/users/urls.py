from django.urls import path
from .views import UserListCreateView, UserRetrieveUpdateDestroyView, GetActiveUsers

urlpatterns = [
    path("user/active/", GetActiveUsers.as_view(), name="active-user-list-create-endpoint"),
    path("user/", UserListCreateView.as_view(), name="user-list-create-endpoint"),
    path("user/<str:telegram_id>/", UserRetrieveUpdateDestroyView.as_view(), name="user-retrieve-update-destroy-endpoint"),
]