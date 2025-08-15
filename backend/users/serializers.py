from rest_framework.serializers import ModelSerializer
from users.models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "telegram_id", "created_at", "is_admin", "updated_at", "is_alive"]
        read_only_fields = ["id", "created_at", "is_admin", "updated_at"]
