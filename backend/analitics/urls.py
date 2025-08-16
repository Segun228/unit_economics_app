from django.urls import path
from . import views

urlpatterns = [
    # ---------------- REPORT ----------------
    path('report/unit/<int:unit_id>/text/', views.UnitTextReportView.as_view(), name='report_unit_text'),
    path('report/set/<int:set_id>/text/', views.SetTextReportView.as_view(), name='report_set_text'),

    path('report/unit/<int:unit_id>/xlsx/', views.UnitExelReportView.as_view(), name='report_unit_xlsx'),
    path('report/set/<int:set_id>/xlsx/', views.SetExelReportView.as_view(), name='report_set_xlsx'),

    path('report/unit/<int:unit_id>/image/', views.UnitImageReportView.as_view(), name='report_unit_image'),
    path('report/set/<int:set_id>/image/', views.SetImageReportView.as_view(), name='report_set_image'),

    # ---------------- EVALUATE ----------------
    path('evaluate/unit/<int:unit_id>/break_even_point/', views.UnitCountBEPView.as_view(), name='evaluate_unit_bep'),
    path('evaluate/unit/<int:unit_id>/required_investments/', views.UnitCountRIView.as_view(), name='evaluate_unit_ri'),
    path('evaluate/unit/<int:unit_id>/expected_profit/', views.UnitCountEPView.as_view(), name='evaluate_unit_ep'),

    path('evaluate/set/<int:set_id>/break_even_point/', views.SetCountBEPView.as_view(), name='evaluate_set_bep'),
    path('evaluate/set/<int:set_id>/required_investments/', views.SetCountRIView.as_view(), name='evaluate_set_ri'),
    path('evaluate/set/<int:set_id>/expected_profit/', views.SetCountEPView.as_view(), name='evaluate_set_ep'),

    # ---------------- GET KPI ----------------
    path('get_kpi/unit/<int:unit_id>/break_even_point/', views.UnitKPICountBEPView.as_view(), name='kpi_unit_bep'),
    path('get_kpi/unit/<int:unit_id>/required_investments/', views.UnitKPICountRIView.as_view(), name='kpi_unit_ri'),
    path('get_kpi/unit/<int:unit_id>/expected_profit/', views.UnitKPICountEPView.as_view(), name='kpi_unit_ep'),
]