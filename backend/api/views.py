
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from api.models import UnitModel, ModelSet
from rest_framework.permissions import AllowAny, IsAuthenticated

from .serializers import ModelSetReadSerializer, ModelSetSerializer, UnitModelSerializer

from .permissions import IsAdminOrDebugOrReadOnly

from backend.authentication import TelegramAuthentication


from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
import logging

from kafka_producer.utils import build_log_message

from rest_framework.response import Response
from rest_framework import mixins, generics



class LoggingRetrieveUpdateDestroyAPIView(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView
):
    """
    View с логированием CRUD операций.
    """
    def log_crud_action(self, request, response, action):
        try:
            build_log_message(
                is_authenticated=request.user.is_authenticated,
                telegram_id=request.user.telegram_id,
                user_id=request.user.id,
                action=action,
                request_method=request.method,
                response_code=response.status_code,
                request_body=getattr(request, "data", None),
            )
        except Exception as e:
            logging.error(f"Failed to log action {action}: {e}")

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        self.log_crud_action(request, response, "retrieve")
        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        self.log_crud_action(request, response, "update")
        return response

    def partial_update(self, request, *args, **kwargs):
        response = super().partial_update(request, *args, **kwargs)
        self.log_crud_action(request, response, "partial_update")
        return response

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        self.log_crud_action(request, response, "destroy")
        return response


class LoggingListCreateAPIView(mixins.ListModelMixin,
                              mixins.CreateModelMixin,
                              generics.GenericAPIView):
    """
    List or create view with logging
    """
    def log_crud_action(self, request, response, action, serializer=None):
        try:
            build_log_message(
                is_authenticated=request.user.is_authenticated,
                telegram_id=getattr(request.user, "telegram_id", None),
                user_id=request.user.id,
                action=action,
                request_method=request.method,
                response_code=response.status_code,
                request_body=serializer.validated_data if serializer else request.data,
            )
        except Exception as e:
            logging.error(f"Failed to log action {action}: {e}")

    def get(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        self.log_crud_action(request, response, action="list")
        return response

    def post(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=False)
        self.log_crud_action(request, response, serializer=serializer, action="create")
        return response


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
        try:
            build_log_message(
                user_id= self.request.user.id,
                is_authenticated= self.request.user.is_authenticated,
                telegram_id= self.request.user.telegram_id,
                action= "create",
                request_body= serializer.validated_data,
                request_method= "POST",
                response_code=201,
            )
        except Exception as e:
            logging.error("Error while sending log via Kafka")
            logging.error(e)


    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        try:
            build_log_message(
                user_id= self.request.user.id,
                is_authenticated= self.request.user.is_authenticated,
                telegram_id= self.request.user.telegram_id,
                action= "sets listed",
                request_body= serializer.data,
                request_method= "GET",
                response_code=200,
            )
        except Exception as e:
            logging.error("Error while sending log via Kafka")
            logging.error(e)

        return Response(serializer.data)


class RetrieveUpdateDestroyModelSetView(AuthenticatedAPIView, LoggingRetrieveUpdateDestroyAPIView):
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
        if set_id is None:
            logging.error("set_id не передан в URL")
            raise Exception("set_id не передан в URL")
        return UnitModel.objects.filter(model_set_id=set_id, user=self.request.user)
