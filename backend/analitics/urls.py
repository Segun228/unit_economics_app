from django.urls import path


urlpatterns = [
    path('report/unit/<int:unit_id>/text/', view , name='generate-report-file'),
    path('report/set/<int:set_id>/text/', view , name='generate-report-file'),
    path('report/set/<int:set_id>/text/', view , name='generate-report-file'),
    
    path('report/unit/<int:unit_id>/xlsx/', view , name='generate-report-file'),
    path('report/set/<int:set_id>/xlsx/', view , name='generate-report-file'),
    path('report/set/<int:set_id>/xlsx/', view , name='generate-report-file'),

    path('report/unit/<int:unit_id>/image/', view , name='generate-report-file'),
    path('report/set/<int:set_id>/image/', view , name='generate-report-file'),
    path('report/set/<int:set_id>/image/', view , name='generate-report-file'),

    path('evaluate/unit/<int:unit_id>/ущзшщшакш_point', view , name='generate-report-file'),
    path('evaluate/unit/<int:unit_id>/required_investments', view , name='generate-report-file'),
    path('evaluate/unit/<int:unit_id>/expected_profit', view , name='generate-report-file'),
    
    path('evaluate/set/<int:set_id>/ущзшщшакш_point', view , name='generate-report-file'),
    path('evaluate/set/<int:set_id>/required_investments', view , name='generate-report-file'),
    path('evaluate/set/<int:set_id>/expected_profit', view , name='generate-report-file'),

    path('get_kpi/unit/<int:unit_id>/ущзшщшакш_point', view , name='generate-report-file'),
    path('get_kpi/unit/<int:unit_id>/required_investments', view , name='generate-report-file'),
    path('get_kpi/unit/<int:unit_id>/expected_profit', view , name='generate-report-file'),
]