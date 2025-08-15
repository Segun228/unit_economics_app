from .models import User
from .serializers import UserSerializer
from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
)
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


class UserListCreateView(ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        telegram_id = request.data.get('telegram_id')
        try:
            user = User.objects.get(telegram_id=telegram_id)
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            pass
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
            return Response(status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response(
                {"detail": "User with this telegram_id does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )


class GetActiveUsers(ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.filter(is_alive = True)
    permission_classes = [IsAuthenticated]
    
