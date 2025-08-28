from .models import User
from .serializers import UserSerializer
from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
)
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from kafka_producer.utils import build_log_message

from django.core.cache import cache
from django.core.cache import cache

class UserListCreateView(ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        telegram_id = request.data.get('telegram_id')
        try:
            user = User.objects.get(telegram_id=telegram_id)
            serializer = self.get_serializer(user)
            build_log_message(
                is_authenticated=request.user.is_authenticated,
                telegram_id=getattr(request.user, "telegram_id", None),
                user_id=request.user.id,
                action="login_user",
                request_method=request.method,
                response_code=200,
                request_body=request.data,
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            pass
            build_log_message(
                is_authenticated=request.user.is_authenticated,
                telegram_id=getattr(request.user, "telegram_id", None),
                user_id=request.user.id,
                action="register",
                request_method=request.method,
                response_code=201,
                request_body=request.data,
            )
        return super().post(request, *args, **kwargs)


class UserRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    def get_object(self):
        if 'telegram_id' in self.kwargs:
            return self.queryset.get(telegram_id=self.kwargs['telegram_id'])
        
        return super().get_object()

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            build_log_message(
                is_authenticated=request.user.is_authenticated,
                telegram_id=getattr(request.user, "telegram_id", None),
                user_id=request.user.id,
                action="delete_user",
                request_method=request.method,
                response_code=201,
                request_body=request.data,
            )
            return Response(status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response(
                {"detail": "User with this telegram_id does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )

    def patch(self, request, *args, **kwargs):
        build_log_message(
            is_authenticated=request.user.is_authenticated,
            telegram_id=getattr(request.user, "telegram_id", None),
            user_id=request.user.id,
            action="partial_update_user",
            request_method=request.method,
            response_code=201,
            request_body=request.data,
        )
        return self.partial_update(request, *args, **kwargs)


class GetActiveUsers(ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.filter(is_alive = True)
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        users = cache.get("users")
        if users:
            return Response(users)
        build_log_message(
            is_authenticated=request.user.is_authenticated,
            telegram_id=getattr(request.user, "telegram_id", None),
            user_id=request.user.id,
            action="list_user",
            request_method=request.method,
            response_code=201,
            request_body=request.data,
        )
        cache.set(
            key="users",
            value=self.list(request, *args, **kwargs)
        )
        return self.list(request, *args, **kwargs)
