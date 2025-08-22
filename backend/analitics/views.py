
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

from .handlers import handlers, report_handlers

from rest_framework.views import APIView


# ───────────────────────────────────────────────
# 🔤 TEXT REPORTS
# ───────────────────────────────────────────────

class AuthView(APIView):
    authentication_classes = [TelegramAuthentication]
    permission_classes = [IsAuthenticated]

class UnitTextReportView(AuthView, APIView):
    def post(self, request, *args, **kwargs):
        unit_id = kwargs.get("unit_id")
        print("unit_id:", unit_id)
        try:
            unit = UnitModel.objects.get(pk=unit_id, user=request.user)
        except UnitModel.DoesNotExist:
            return Response({"error": "Unit not found"}, status=404)
        data = UnitModelSerializer(unit).data
        result = report_handlers.unit_calculate_economics(data = data)
        return Response(result)


class SetTextReportView(AuthView, APIView):
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

class UnitExelReportView(AuthView, APIView):
    def post(self, request, *args, **kwargs):
        unit_id = int(kwargs.get("unit_id"))
        try:
            unit = UnitModel.objects.get(pk=unit_id)
        except UnitModel.DoesNotExist:
            return Response({"error": "Unit not found"}, status=404)
        data = UnitModelSerializer(unit).data


class SetExelReportView(AuthView, APIView):
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

class UnitImageReportView(AuthView, APIView):
    def post(self, request, *args, **kwargs):
        unit_id = kwargs.get("unit_id")
        try:
            unit = UnitModel.objects.get(pk=unit_id)
        except UnitModel.DoesNotExist:
            return Response({"error": "Unit not found"}, status=404)
        data = UnitModelSerializer(unit).data


class SetImageReportView(AuthView, APIView):
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

class UnitCountBEPView(AuthView, APIView):
    def post(self, request, *args, **kwargs):
        unit_id = kwargs.get("unit_id")
        try:
            unit = UnitModel.objects.get(pk=unit_id)
        except UnitModel.DoesNotExist:
            return Response({"error": "Unit not found"}, status=404)
        data = UnitModelSerializer(unit).data


class UnitCountRIView(AuthView, APIView):
    def post(self, request, *args, **kwargs):
        unit_id = kwargs.get("unit_id")
        try:
            unit = UnitModel.objects.get(pk=unit_id)
        except UnitModel.DoesNotExist:
            return Response({"error": "Unit not found"}, status=404)
        data = UnitModelSerializer(unit).data


class UnitCountEPView(AuthView, APIView):
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

class SetCountBEPView(AuthView, APIView):
    def post(self, request, *args, **kwargs):
        set_id = kwargs.get("set_id")
        try:
            set = ModelSet.objects.get(pk=set_id)
        except ModelSet.DoesNotExist:
            return Response({"error": "Unit not found"}, status=404)
        data = UnitModelSerializer(set).data


class SetCountRIView(AuthView, APIView):
    def post(self, request, *args, **kwargs):
        set_id = kwargs.get("set_id")
        try:
            set = ModelSet.objects.get(pk=set_id)
        except ModelSet.DoesNotExist:
            return Response({"error": "Unit not found"}, status=404)
        data = UnitModelSerializer(set).data


class SetCountEPView(AuthView, APIView):
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

class UnitKPICountBEPView(AuthView, APIView):
    def post(self, request, *args, **kwargs):
        unit_id = kwargs.get("unit_id")
        try:
            unit = UnitModel.objects.get(pk=unit_id)
        except UnitModel.DoesNotExist:
            return Response({"error": "Unit not found"}, status=404)
        data = UnitModelSerializer(unit).data


class UnitKPICountRIView(AuthView, APIView):
    def post(self, request, *args, **kwargs):
        unit_id = kwargs.get("unit_id")
        try:
            unit = UnitModel.objects.get(pk=unit_id)
        except UnitModel.DoesNotExist:
            return Response({"error": "Unit not found"}, status=404)
        data = UnitModelSerializer(unit).data


class UnitKPICountEPView(AuthView, APIView):
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

class FileUploadView(AuthView, APIView):
    authentication_classes = [TelegramAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        units = UnitModel.objects.filter(user = request.user).values()
        sets = ModelSet.objects.filter(user = request.user).values()
        return handlers.get_xlsx_report(
            units = units,
            sets = sets
        )

    def post(self, request, *args, **kwargs):
        excel_file = request.FILES.get("file")
        name = request.data.get("name", "New set via XLSX")
        if not excel_file:
            return Response({"error": "Файл не передан"}, status=400)
        result = handlers.add_posts_file(data = excel_file, request= request, name = name)
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

class GetFileDatabase(AuthView, APIView):
    authentication_classes = [TelegramAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        units = UnitModel.objects.filter(user = request.user).values()
        sets = ModelSet.objects.filter(user = request.user).values()
        return handlers.get_xlsx_report(
            units = units,
            sets = sets
        )


