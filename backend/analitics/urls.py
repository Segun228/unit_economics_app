from django.urls import path
from . import views

urlpatterns = [
    # ---------------- REPORT ----------------
    path('report/unit/<int:unit_id>/text/', views.UnitTextReportView.as_view(), name='report_unit_text'),
    path('report/set/<int:set_id>/text/', views.SetTextReportView.as_view(), name='report_set_text'),

    path('report/set/<int:set_id>/image/', views.SetImageReportView.as_view(), name='report_set_image'),

    path('report/unit/<int:unit_id>/xlsx/', views.UnitExelReportView.as_view(), name='report_unit_xlsx'),
    path('report/set/<int:set_id>/xlsx/', views.SetExelReportView.as_view(), name='report_set_xlsx'),


    # ---------------- EVALUATE ----------------
    path('evaluate/unit/<int:unit_id>/break_even_point/', views.UnitCountBEPView.as_view(), name='evaluate_unit_bep'),
    path('evaluate/set/<int:set_id>/break_even_point/', views.SetCountBEPView.as_view(), name='evaluate_set_bep'),

    # ---------------- COHORT ----------------
    path('cohort/unit/<int:unit_id>/', views.UnitCohortView.as_view(), name='unit_cohort_analisis'),
    path('cohort/set/<int:set_id>/', views.SetCohortView.as_view(), name='set_chohort_analisis'),
    # ---------------- SCAN EXCEL ----------------
    path('file/upload/', views.FileUploadView.as_view(), name='file_upload_endpoint'),
]