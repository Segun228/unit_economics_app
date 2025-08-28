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
# CACHED REQUESTS SCHEMA
# ───────────────────────────────────────────────
"""
    f"model_{unit_id}_text_report_user_{request.user.id}" - unit text report
    f"set_{set_id}_text_report_user_{request.user.id}"

    f"model_{unit_id}_exel_report_user_{request.user.id}" - unit exel report
    f"set_{set_id}_exel_report_user_{request.user.id}" - set exel report

    f"set_{set_id}_image_report_user_{request.user.id}" - set image report
    f"model_{unit_id}_bep_report_user_{request.user.id}" - unit bep report

    f"model_{unit_id}_cohort_report_user_{request.user.id}" - unit cohort report
    f"set_{set_id}_cohort_report_user_{request.user.id}" - set cohort report

    f"db_report_user_{request.user.id}" - database report
"""
# ───────────────────────────────────────────────
# 🔤 TEXT REPORTS
# ───────────────────────────────────────────────

class AuthView(APIView):
    authentication_classes = [TelegramAuthentication]
    permission_classes = [IsAuthenticated]

class UnitTextReportView(AuthView, APIView):
    def post(self, request, *args, **kwargs):
        unit_id = kwargs.get("unit_id")
        cached = cache.get(key=f"model_{unit_id}_text_report_user_{request.user.id}")
        if cached:
            return Response(cached)
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
        cache.set(
            key=f"model_{unit_id}_text_report_user_{request.user.id}",
            value=result
        )
        return Response(result)


class SetTextReportView(AuthView, APIView):
    def post(self, request, *args, **kwargs):
        set_id = kwargs.get("set_id")
        cached = cache.get(key=f"set_{set_id}_text_report_user_{request.user.id}")
        if cached:
            return Response(cached)
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
            result = report_handlers.set_calculate_economics(data = data)
            cache.set(
                key=f"set_{set_id}_text_report_user_{request.user.id}",
                value=result.data
            )
            return result
        except ModelSet.DoesNotExist:
            return Response({"error": "Set not found"}, status=404)
        except Exception as e:
            logging.exception("Error while generating Unit report")
            return Response({"error": str(e)}, status=500)


# ───────────────────────────────────────────────
# 📄 EXCEL REPORTS
# ───────────────────────────────────────────────

class UnitExelReportView(AuthView, APIView):
    def post(self, request, *args, **kwargs):
        unit_id = kwargs.get("unit_id")
        resp = cache.get(
            key=f"model_{unit_id}_exel_report_user_{request.user.id}"
        )
        try:
            unit = UnitModel.objects.get(pk=unit_id, user=request.user)
        except UnitModel.DoesNotExist:
            return Response({"error": "Unit not found"}, status=404)
        if resp:
            response = HttpResponse(
                resp,
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = f'attachment; filename={unit.name if unit else "Model"}.xlsx'
            return response

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
            cache.set(
                key=f"model_{unit_id}_exel_report_user_{request.user.id}",
                value = result[1]
            )
            return result[0]
        except Exception as e:
            logging.exception(e)
            return Response({"error": f"An error occured {e}"}, status=404)


class SetExelReportView(AuthView, APIView):
    def post(self, request, *args, **kwargs):
        set_id = kwargs.get("set_id")
        set = ModelSet.objects.get(pk=set_id, user=request.user)
        resp = cache.get(
            key=f"set_{set_id}_exel_report_user_{request.user.id}"
        )
        if resp:
            response = HttpResponse(
                resp,
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = f'attachment; filename={set.name if set else "Set"}.xlsx'
            return response
        try:
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
            result = set_handlers.set_generate_report(data = data)
            cache.set(
                key=f"set_{set_id}_exel_report_user_{request.user.id}",
                value = result[1]
            )
            return result[0]
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
        resp = cache.get(
            key=f"set_{set_id}_image_report_user_{request.user.id}"
        )
        if resp:
            response = HttpResponse(resp, content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename="report_bundle.zip"'
            return response
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
            result = report_handlers.set_visualize(data = data)
            cache.set(
                key=f"set_{set_id}_image_report_user_{request.user.id}",
                value=result[1]
            )
            return result[0]
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
        resp = cache.get(
            key=f"model_{unit_id}_bep_report_user_{request.user.id}"
        )
        if resp:
            return HttpResponse(resp, content_type='image/png')
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
        cache.set(
            key=f"model_{unit_id}_bep_report_user_{request.user.id}",
            value=buf.getvalue()
        )
        return HttpResponse(buf.getvalue(), content_type='image/png')


# ───────────────────────────────────────────────
# 📤 COHORT ANALISIS
# ───────────────────────────────────────────────

class UnitCohortView(AuthView, APIView):
    def post(self, request, *args, **kwargs):
        unit_id = kwargs.get("unit_id")
        resp = cache.get(f"model_{unit_id}_cohort_report_user_{request.user.id}")
        if resp:
            response = HttpResponse(resp, content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename="report_bundle.zip"'
            return response
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
            resp = unit_handlers.unit_count_cohort(data=data)
            cache.set(
                f"model_{unit_id}_cohort_report_user_{request.user.id}",
                value= resp[1]
            )
            return resp[0]
        except Exception as e:
            logging.exception(f"Error generating plot: {e}")
            return Response({"error": "Error while generating plot"}, status=400)


class SetCohortView(AuthView, APIView):
    def post(self, request, *args, **kwargs):
        set_id = kwargs.get("set_id")
        cash = cache.get(f"set_{set_id}_cohort_report_user_{request.user.id}")
        if cash:
            response = HttpResponse(cash, content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename="report_bundle.zip"'
            return response
        try:
            set = ModelSet.objects.get(pk=set_id, user=request.user)
        except ModelSet.DoesNotExist:
            return Response({"error": "Set not found"}, status=404)

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
            res = set_handlers.set_count_cohort(data=data)
            cache.set(
                f"set_{set_id}_cohort_report_user_{request.user.id}",
                value= res[1]
            )
            return res[0]
        except Exception as e:
            logging.exception(f"Error generating plot: {e}")
            return Response({"error": "Error while generating plot"}, status=400)

# ───────────────────────────────────────────────
# 📤 FILE UPLOAD
# ───────────────────────────────────────────────

class FileUploadView(AuthView, APIView):
    authentication_classes = [TelegramAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        cash = cache.get(f"db_report_user_{request.user.id}")
        if cash:
            response = HttpResponse(
                cash,
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = 'attachment; filename=products.xlsx'
            return response
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
        res = handlers.get_xlsx_report(
            units = units,
            sets = sets
        )
        if isinstance(res, HttpResponseBadRequest):
            return res
        cache.set(
            key=f"db_report_user_{request.user.id}",
            value=res[1]
        )
        return res[0]

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
        cash = cache.get(f"db_report_user_{request.user.id}")
        if cash:
            response = HttpResponse(
                cash,
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = 'attachment; filename=products.xlsx'
            return response
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
        res = handlers.get_xlsx_report(
            units = units,
            sets = sets
        )
        if isinstance(res, HttpResponseBadRequest):
            return res
        cache.set(
            key=f"db_report_user_{request.user.id}",
            value=res[1]
        )
        return res[0]

