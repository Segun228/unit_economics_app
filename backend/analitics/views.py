from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView
)
from rest_framework.permissions import AllowAny, IsAuthenticated

from django.http import HttpResponseBadRequest, JsonResponse

from rest_framework import status
from rest_framework.response import Response

from api.models import ModelSet, UnitModel

from api.serializers import (
    UnitModelSerializer,
    ModelSetReadSerializer
)

from backend.authentication import TelegramAuthentication

from rest_framework.response import Response

from .permissions import IsAdminCustom

from .handlers import handlers



# ───────────────────────────────────────────────
# 🔤 TEXT REPORTS
# ───────────────────────────────────────────────

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


# ───────────────────────────────────────────────
# 📄 EXCEL REPORTS
# ───────────────────────────────────────────────

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


# ───────────────────────────────────────────────
# 🖼️ IMAGE REPORTS
# ───────────────────────────────────────────────

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


# ───────────────────────────────────────────────
# 📊 UNIT KPI BASIC CALCULATIONS (BEP, RI, EP)
# ───────────────────────────────────────────────

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


# ───────────────────────────────────────────────
# 📊 SET KPI BASIC CALCULATIONS (BEP, RI, EP)
# ───────────────────────────────────────────────

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


# ───────────────────────────────────────────────
# 📈 KPI EXTENDED: UNIT-LEVEL METRICS (KPI по каждому юниту)
# ───────────────────────────────────────────────

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


# ───────────────────────────────────────────────
# 📤 FILE UPLOAD
# ───────────────────────────────────────────────

class FileUploadView(ListCreateAPIView):
    authentication_classes = [TelegramAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        excel_file = request.FILES.get("file")
        if not excel_file:
            return Response({"error": "Файл не передан"}, status=400)
        result = handlers.add_posts_file(data = excel_file, request= request)
        if not result:
            return HttpResponseBadRequest()
        if result['errors']:
            return Response(
                {
                    "success": result['success'],
                    "errors": result['errors']
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            return Response(
                {"success": result['success']},
                status=status.HTTP_200_OK
            )


# ───────────────────────────────────────────────
# 📥 GET FULL XLSX EXPORT FROM DB
# ───────────────────────────────────────────────

class GetFileDatabase(ListCreateAPIView):
    authentication_classes = [TelegramAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        units = UnitModel.objects.filter(user = request.user).values()
        sets = ModelSet.objects.filter(user = request.user).values()
        return handlers.get_xlsx_report(
            units = units,
            sets = sets
        )


