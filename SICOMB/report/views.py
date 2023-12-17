from django.shortcuts import render
from .models import *

def filterReport(request):
    data = {
        'reports': Report.objects.all(),
    }
    
    return render(request, 'report/filter-report.html', data)

def getReportPage(request, id):
    data = {
        'report': Report.objects.filter(id=id).first(),
    }
    
    return render(request, 'report/report.html', data)


def getPdfFile(request, id):
    
    return Report.objects.filter(id=id).first().generatePDF()