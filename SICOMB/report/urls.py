from django.urls import path
from . import views

urlpatterns = [
    path("", views.filterReport, name='relatorios'),
    path("<int:id>/", views.getReportPage, name='relatorio'),
    path("get_pdf_file/<int:id>/", views.getPdfFile, name='relatorio'),
]