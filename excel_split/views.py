from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, FileResponse
# from django.views import generic
from django.shortcuts import render
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../")
from exceltools.excel_spliter.excel_spliter import excelSplitBySheet
from django import forms
import zipfile
from os.path import basename


def handle_uploaded_file(f):
    with open("./excel_split/upload/%s" % f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return "./excel_split/upload/%s" % f.name

def index(request):
    template_name = 'excel_split/index.html'
    context = {}
    return render(request, template_name, context)

class UploadFileForm(forms.Form):
    excel = forms.FileField()
    sheetNum = forms.NumberInput()
    sheetNameKey = forms.CharField(required=False)
    headLines = forms.NumberInput()
    columnLabels = forms.CharField(max_length=50)
    # allSheet = forms.BooleanField(required=False)

def split(request):
    # print(request.POST)
    # print(request.FILES)
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # save excel
            savedExcel = handle_uploaded_file(request.FILES['excel'])
            print(savedExcel)
            # split excel
            columnLabels = request.POST['columnLabels']
            headLines = int(request.POST['headLines'])
            sheetNum = int(request.POST["sheetNum"])
            sheetNameKey = request.POST['sheetNameKey']
            allSheet = 'allSheet' in request.POST
            print(allSheet)
            outputPath, err = excelSplitBySheet(savedExcel, columnLabels=columnLabels, headLines=headLines, \
                              sheetNum=sheetNum, sheetNameKey=sheetNameKey, allSheet=allSheet)
            print(outputPath)
            # zip excel
            zip_file = ".".join(savedExcel.split(".")[:-1]) + "_split_by_%s.zip" % columnLabels
            zip = zipfile.ZipFile(zip_file, 'w')
            for f in os.listdir(outputPath):
                zip.write(os.path.join(outputPath, f), f, zipfile.ZIP_DEFLATED)
            zip.close()
            # return zip file
            download_file = open(zip_file, 'rb')
            print(basename(zip_file))
            response = FileResponse(download_file)
            response['Content-Type'] = 'application/zip'
            response['Content-Disposition'] = "attachment;filename=%s" % basename(zip_file).encode('utf-8').decode('ISO-8859-1')
            return response
        else:
            return HttpResponse("form wrong")
    else:
        return HttpResponse("need post")

