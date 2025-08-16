from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView
)
from rest_framework.permissions import AllowAny, IsAuthenticated

from api.models import ModelSet, UnitModel

from api.serializers import (
    UnitModelSerializer,
    ModelSetReadSerializer
)

from backend.authentication import TelegramAuthentication

from rest_framework.response import Response


class UnitTextReportView(ListCreateAPIView):
    def post(self, request, *args, **kwargs):
        unit_id = kwargs.get("unit_id")
        try:
            unit = UnitModel.objects.get(pk=unit_id)
        except UnitModel.DoesNotExist:
            return Response({"error": "Unit not found"}, status=404)
        data = UnitModelSerializer(unit).data


class SetTextReportView(ListCreateAPIView):
    def post(self, request, *args, **kwargs):
        set_id = kwargs.get("set_id")
        try:
            set = ModelSet.objects.get(pk=set_id)
        except ModelSet.DoesNotExist:
            return Response({"error": "Unit not found"}, status=404)
        data = UnitModelSerializer(set).data


class UnitExelReportView(ListCreateAPIView):
    def post(self, request, *args, **kwargs):
        unit_id = kwargs.get("unit_id")
        try:
            unit = UnitModel.objects.get(pk=unit_id)
        except UnitModel.DoesNotExist:
            return Response({"error": "Unit not found"}, status=404)
        data = UnitModelSerializer(unit).data


class SetExelReportView(ListCreateAPIView):
    def post(self, request, *args, **kwargs):
        set_id = kwargs.get("set_id")
        try:
            set = ModelSet.objects.get(pk=set_id)
        except ModelSet.DoesNotExist:
            return Response({"error": "Unit not found"}, status=404)
        data = UnitModelSerializer(set).data


class UnitImageReportView(ListCreateAPIView):
    def post(self, request, *args, **kwargs):
        unit_id = kwargs.get("unit_id")
        try:
            unit = UnitModel.objects.get(pk=unit_id)
        except UnitModel.DoesNotExist:
            return Response({"error": "Unit not found"}, status=404)
        data = UnitModelSerializer(unit).data


class SetImageReportView(ListCreateAPIView):
    def post(self, request, *args, **kwargs):
        set_id = kwargs.get("set_id")
        try:
            set = ModelSet.objects.get(pk=set_id)
        except ModelSet.DoesNotExist:
            return Response({"error": "Unit not found"}, status=404)
        data = UnitModelSerializer(set).data


class UnitCountBEPView(ListCreateAPIView):
    def post(self, request, *args, **kwargs):
        unit_id = kwargs.get("unit_id")
        try:
            unit = UnitModel.objects.get(pk=unit_id)
        except UnitModel.DoesNotExist:
            return Response({"error": "Unit not found"}, status=404)
        data = UnitModelSerializer(unit).data


class UnitCountRIView(ListCreateAPIView):
    def post(self, request, *args, **kwargs):
        unit_id = kwargs.get("unit_id")
        try:
            unit = UnitModel.objects.get(pk=unit_id)
        except UnitModel.DoesNotExist:
            return Response({"error": "Unit not found"}, status=404)
        data = UnitModelSerializer(unit).data


class UnitCountEPView(ListCreateAPIView):
    def post(self, request, *args, **kwargs):
        unit_id = kwargs.get("unit_id")
        try:
            unit = UnitModel.objects.get(pk=unit_id)
        except UnitModel.DoesNotExist:
            return Response({"error": "Unit not found"}, status=404)
        data = UnitModelSerializer(unit).data


class SetCountBEPView(ListCreateAPIView):
    def post(self, request, *args, **kwargs):
        set_id = kwargs.get("set_id")
        try:
            set = ModelSet.objects.get(pk=set_id)
        except ModelSet.DoesNotExist:
            return Response({"error": "Unit not found"}, status=404)
        data = UnitModelSerializer(set).data


class SetCountRIView(ListCreateAPIView):
    def post(self, request, *args, **kwargs):
        set_id = kwargs.get("set_id")
        try:
            set = ModelSet.objects.get(pk=set_id)
        except ModelSet.DoesNotExist:
            return Response({"error": "Unit not found"}, status=404)
        data = UnitModelSerializer(set).data


class SetCountEPView(ListCreateAPIView):
    def post(self, request, *args, **kwargs):
        set_id = kwargs.get("set_id")
        try:
            set = ModelSet.objects.get(pk=set_id)
        except ModelSet.DoesNotExist:
            return Response({"error": "Unit not found"}, status=404)
        data = UnitModelSerializer(set).data


class UnitKPICountBEPView(ListCreateAPIView):
    def post(self, request, *args, **kwargs):
        unit_id = kwargs.get("unit_id")
        try:
            unit = UnitModel.objects.get(pk=unit_id)
        except UnitModel.DoesNotExist:
            return Response({"error": "Unit not found"}, status=404)
        data = UnitModelSerializer(unit).data


class UnitKPICountRIView(ListCreateAPIView):
    def post(self, request, *args, **kwargs):
        unit_id = kwargs.get("unit_id")
        try:
            unit = UnitModel.objects.get(pk=unit_id)
        except UnitModel.DoesNotExist:
            return Response({"error": "Unit not found"}, status=404)
        data = UnitModelSerializer(unit).data


class UnitKPICountEPView(ListCreateAPIView):
    def post(self, request, *args, **kwargs):
        unit_id = kwargs.get("unit_id")
        try:
            unit = UnitModel.objects.get(pk=unit_id)
        except UnitModel.DoesNotExist:
            return Response({"error": "Unit not found"}, status=404)
        data = UnitModelSerializer(unit).data


