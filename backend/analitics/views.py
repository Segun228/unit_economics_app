import logging
from rest_framework.permissions import AllowAny, IsAuthenticated

from django.http import HttpResponseBadRequest, JsonResponse

from rest_framework import status
from rest_framework.response import Response

from rest_framework.exceptions import bad_request

from api.models import ModelSet, UnitModel

from api.serializers import (
    UnitModelSerializer,
    ModelSetReadSerializer
)

from backend.authentication import TelegramAuthentication

from rest_framework.response import Response

from .permissions import IsAdminCustom

from .handlers import handlers, report_handlers, unit_handlers, set_handlers

from rest_framework.views import APIView

from django.http import HttpResponse

from kafka_producer.utils import build_log_message

from django.core.cache import cache


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
        build_log_message(
            is_authenticated=request.user.is_authenticated,
            telegram_id=getattr(request.user, "telegram_id", None),
            user_id=request.user.id,
            action="unit_text_report",
            request_method=request.method,
            response_code=200,
            request_body= request.data,
        )
        return Response(result)


class SetTextReportView(AuthView, APIView):
    def post(self, request, *args, **kwargs):
        set_id = kwargs.get("set_id")
        try:
            set = ModelSet.objects.get(pk=set_id, user=request.user)
            data = ModelSetReadSerializer(set).data
            build_log_message(
                is_authenticated=request.user.is_authenticated,
                telegram_id=getattr(request.user, "telegram_id", None),
                user_id=request.user.id,
                action="set_text_report",
                request_method=request.method,
                response_code=200,
                request_body= request.data,
            )
            return report_handlers.set_calculate_economics(data = data)
        except ModelSet.DoesNotExist:
            return Response({"error": "Set not found"}, status=404)
        except Exception as e:
            logging.exception(e)
            raise


# ───────────────────────────────────────────────
# 📄 EXCEL REPORTS
# ───────────────────────────────────────────────

class UnitExelReportView(AuthView, APIView):
    def post(self, request, *args, **kwargs):
        unit_id = kwargs.get("unit_id")
        try:
            unit = UnitModel.objects.get(pk=unit_id, user=request.user)
        except UnitModel.DoesNotExist:
            return Response({"error": "Unit not found"}, status=404)
        try:
            data = UnitModelSerializer(unit).data
            result = unit_handlers.unit_generate_report(data=data)
            build_log_message(
                is_authenticated=request.user.is_authenticated,
                telegram_id=getattr(request.user, "telegram_id", None),
                user_id=request.user.id,
                action="unit_exel_report",
                request_method=request.method,
                response_code=200,
                request_body= request.data,
            )
            return result
        except Exception as e:
            logging.exception(e)
            return Response({"error": f"An error occured {e}"}, status=404)


class SetExelReportView(AuthView, APIView):
    def post(self, request, *args, **kwargs):
        set_id = kwargs.get("set_id")
        try:
            set = ModelSet.objects.get(pk=set_id, user=request.user)
            data = ModelSetReadSerializer(set).data
            build_log_message(
                is_authenticated=request.user.is_authenticated,
                telegram_id=getattr(request.user, "telegram_id", None),
                user_id=request.user.id,
                action="set_exel_report",
                request_method=request.method,
                response_code=200,
                request_body= request.data,
            )
            return set_handlers.set_generate_report(data = data)
        except ModelSet.DoesNotExist:
            return Response({"error": "Set not found"}, status=404)
        except Exception as e:
            logging.exception(e)
            raise


# ───────────────────────────────────────────────
# 🖼️ IMAGE REPORTS
# ───────────────────────────────────────────────



class SetImageReportView(AuthView, APIView):
    def post(self, request, *args, **kwargs):
        set_id = kwargs.get("set_id")
        try:
            set = ModelSet.objects.get(pk=set_id, user=request.user)
            data = ModelSetReadSerializer(set).data
            build_log_message(
                is_authenticated=request.user.is_authenticated,
                telegram_id=getattr(request.user, "telegram_id", None),
                user_id=request.user.id,
                action="set_image_report",
                request_method=request.method,
                response_code=200,
                request_body= request.data,
            )
            return report_handlers.set_visualize(data = data)
        except ModelSet.DoesNotExist:
            return Response({"error": "Set not found"}, status=404)
        except Exception as e:
            logging.exception(e)
            raise


# ───────────────────────────────────────────────
# 📊 UNIT KPI BASIC CALCULATIONS
# ───────────────────────────────────────────────

class UnitCountBEPView(AuthView, APIView):
    def post(self, request, *args, **kwargs):
        unit_id = kwargs.get("unit_id")
        try:
            unit = UnitModel.objects.get(pk=unit_id, user=request.user)
        except UnitModel.DoesNotExist:
            return Response({"error": "Unit not found"}, status=404)

        data = UnitModelSerializer(unit).data
        try:
            proc, buf = unit_handlers.unit_count_bep(data=data)
        except Exception as e:
            logging.error(f"Error generating plot: {e}")
            return Response({"error": "Error while generating plot"}, status=400)

        if not proc or not buf:
            build_log_message(
                is_authenticated=request.user.is_authenticated,
                telegram_id=getattr(request.user, "telegram_id", None),
                user_id=request.user.id,
                action="unit_bep_report",
                request_method=request.method,
                response_code=200,
                request_body= request.data,
            )
            return Response({"error": "Error while generating plot"}, status=400)

        return HttpResponse(buf.getvalue(), content_type='image/png')


# ───────────────────────────────────────────────
# 📤 COHORT ANALISIS
# ───────────────────────────────────────────────

class UnitCohortView(AuthView, APIView):
    def post(self, request, *args, **kwargs):
        unit_id = kwargs.get("unit_id")
        try:
            unit = UnitModel.objects.get(pk=unit_id, user=request.user)
        except UnitModel.DoesNotExist:
            return Response({"error": "Unit not found"}, status=404)

        data = UnitModelSerializer(unit).data
        try:
            build_log_message(
                is_authenticated=request.user.is_authenticated,
                telegram_id=getattr(request.user, "telegram_id", None),
                user_id=request.user.id,
                action="unit_cohort_report",
                request_method=request.method,
                response_code=200,
                request_body= request.data,
            )
            return unit_handlers.unit_count_cohort(data=data)
        except Exception as e:
            logging.exception(f"Error generating plot: {e}")
            return Response({"error": "Error while generating plot"}, status=400)


class SetCohortView(AuthView, APIView):
    def post(self, request, *args, **kwargs):
        set_id = kwargs.get("set_id")
        try:
            set = ModelSet.objects.get(pk=set_id, user=request.user)
        except UnitModel.DoesNotExist:
            return Response({"error": "Unit not found"}, status=404)

        data = ModelSetReadSerializer(set).data
        try:
            build_log_message(
                is_authenticated=request.user.is_authenticated,
                telegram_id=getattr(request.user, "telegram_id", None),
                user_id=request.user.id,
                action="set_cohort_report",
                request_method=request.method,
                response_code=200,
                request_body= request.data,
            )
            return set_handlers.set_count_cohort(data=data)
        except Exception as e:
            logging.exception(f"Error generating plot: {e}")
            return Response({"error": "Error while generating plot"}, status=400)

# ───────────────────────────────────────────────
# 📤 FILE UPLOAD
# ───────────────────────────────────────────────

class FileUploadView(AuthView, APIView):
    authentication_classes = [TelegramAuthentication]
    permission_classes = [IsAuthenticated]
# TODO 
    def get(self, request, *args, **kwargs):
        units = UnitModel.objects.filter(user = request.user).values()
        sets = ModelSet.objects.filter(user = request.user).values()
        build_log_message(
            is_authenticated=request.user.is_authenticated,
            telegram_id=getattr(request.user, "telegram_id", None),
            user_id=request.user.id,
            action="get_db_excel",
            request_method=request.method,
            response_code=200,
            request_body= request.data,
        )
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
            build_log_message(
                is_authenticated=request.user.is_authenticated,
                telegram_id=getattr(request.user, "telegram_id", None),
                user_id=request.user.id,
                action="post_db_excel",
                request_method=request.method,
                response_code=400,
                request_body= request.data,
            )
            return Response(
                {
                    "success": result['success'],
                    "errors": result['errors']
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            build_log_message(
                is_authenticated=request.user.is_authenticated,
                telegram_id=getattr(request.user, "telegram_id", None),
                user_id=request.user.id,
                action="post_db_excel",
                request_method=request.method,
                response_code=200,
                request_body= request.data,
            )
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
        build_log_message(
            is_authenticated=request.user.is_authenticated,
            telegram_id=getattr(request.user, "telegram_id", None),
            user_id=request.user.id,
            action="get_db_excel",
            request_method=request.method,
            response_code=200,
            request_body= request.data,
        )
        return handlers.get_xlsx_report(
            units = units,
            sets = sets
        )


