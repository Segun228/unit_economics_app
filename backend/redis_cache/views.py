from rest_framework.views import APIView
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class CacheView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        result = cache.get(key="example")
        return Response(result)

    def post(self, request, *args, **kwargs):
        cache.set("example", "data", timeout=30)
        val = cache.get("example")
        return Response({"value": val})