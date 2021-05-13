from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, FileResponse
# from django.views import generic
from django.shortcuts import render
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../")
from exceltools.excel_merger.excel_merger import excelMergeBySheet
from django import forms
import time
from os.path import basename


def handle_uploaded_files(files, key):
    path = ""
    for f in files:
        if not key in f.name:
            continue
        # todo: check excel
        if not path:
            path = "./excel_merge/upload/%s_etc_merged_%s" % (basename(".".join(f.name.split(".")[:-1])),
                                                              time.strftime("%Y_%m_%d-%H_%M", time.localtime()))
            if not os.path.exists(path):
                os.mkdir(path)
        with open("%s/%s" % (path, f.name), 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
    return path

def index(request):
    template_name = 'excel_merge/index.html'
    context = {}
    return render(request, template_name, context)

class UploadFileForm(forms.Form):
    excel = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    sheetNum = forms.NumberInput()
    sheetNameKey = forms.CharField(required=False)
    headLines = forms.NumberInput()
    excelNameKey = forms.CharField(max_length=50, required=False)
    # allSheet = forms.BooleanField(required=False)

def merge(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        # print(request.FILES)
        # print(request.FILES.getlist('excel'))
        # return HttpResponse("form wrong")
        if form.is_valid():
            excelNameKey = request.POST['excelNameKey']
            # save excel
            savedExcels = handle_uploaded_files(request.FILES.getlist('excel'), excelNameKey)
            # print(savedExcels)
            # merge excel
            headLines = int(request.POST['headLines'])
            sheetNum = int(request.POST["sheetNum"])
            sheetNameKey = request.POST['sheetNameKey']
            allSheet = 'allSheet' in request.POST
            rmDup = 'rmDup' in request.POST
            styles = 'styles' in request.POST
            outputPath, err = excelMergeBySheet(savedExcels, headLines=headLines, sheetNum=sheetNum,
                                                sheetNameKey=sheetNameKey, allSheet=allSheet, rmDup=rmDup, styles=styles)
            # return file
            download_file = open(outputPath, 'rb')
            response = FileResponse(download_file)
            response['Content-Type'] = 'application/vnd.ms-excel'
            response['Content-Disposition'] = "attachment;filename=%s" % basename(outputPath).encode('utf-8').decode('ISO-8859-1')
            return response
        else:
            return HttpResponse("form wrong")
    else:
        return HttpResponse("need post")