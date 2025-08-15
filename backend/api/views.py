from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from api.models import UnitModel, ModelSet
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import ModelSet, UnitModel

from .serializers import ModelSetReadSerializer, ModelSetSerializer, UnitModelSerializer

from .permissions import IsAdminOrDebugOrReadOnly

from backend.backend.authentication import TelegramAuthentication



class ListCreateModeSetlView(ListCreateAPIView):
    authentication_classes = [TelegramAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = ModelSet.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ModelSetReadSerializer
        return ModelSetSerializer


class RetrieveUpdateDestroyModelSetView(ListCreateAPIView):
    authentication_classes = [TelegramAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = ModelSet.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = 'set_id'

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ModelSetReadSerializer
        return ModelSetSerializer



class ListCreateUnitModelView(ListCreateAPIView):
    authentication_classes = [TelegramAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = UnitModel.objects.all()
    serializer_class = UnitModelSerializer



class RetrieveUpdateDestroyUnitModelView(ListCreateAPIView):
    authentication_classes = [TelegramAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = UnitModel.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = 'set_id'
    serializer_class = UnitModelSerializer

