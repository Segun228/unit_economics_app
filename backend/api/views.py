from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from api.models import UnitModel, ModelSet
from rest_framework.permissions import AllowAny, IsAuthenticated

from .serializers import ModelSetReadSerializer, ModelSetSerializer, UnitModelSerializer

from .permissions import IsAdminOrDebugOrReadOnly

from backend.authentication import TelegramAuthentication


from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404


class AuthenticatedAPIView:
    authentication_classes = [TelegramAuthentication]
    permission_classes = [IsAuthenticated]



class ListCreateModelSetView(AuthenticatedAPIView, ListCreateAPIView):
    def get_queryset(self):
        return ModelSet.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ModelSetReadSerializer
        return ModelSetSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RetrieveUpdateDestroyModelSetView(AuthenticatedAPIView, RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    lookup_url_kwarg = 'set_id'

    def get_queryset(self):
        return ModelSet.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ModelSetReadSerializer
        return ModelSetSerializer



class ListCreateUnitModelView(ListCreateAPIView):
    authentication_classes = [TelegramAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UnitModelSerializer

    def get_queryset(self):
        set_id = self.kwargs.get("set_id")
        return UnitModel.objects.filter(model_set_id=set_id, user=self.request.user)

    def perform_create(self, serializer):
        set_id = self.kwargs.get("set_id")
        model_set = get_object_or_404(ModelSet, id=set_id, user=self.request.user)
        serializer.save(user=self.request.user, model_set=model_set)


class RetrieveUpdateDestroyUnitModelView(AuthenticatedAPIView, RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    lookup_url_kwarg = 'unit_id'
    serializer_class = UnitModelSerializer

    def get_queryset(self):
        set_id = self.kwargs.get("set_id")
        return UnitModel.objects.filter(model_set_id=set_id, user=self.request.user)

