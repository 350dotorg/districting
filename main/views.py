from django.http import (HttpResponse,
                         HttpResponseForbidden, 
                         HttpResponseNotFound)
from django.shortcuts import redirect 
from djangohelpers import (rendered_with,
                           allow_http)

from main.forms import SpreadsheetForm

import csv
import io

CSV_COLUMNS = (
    "node_id",
    "url",
    "first_name",
    "last_name",
    "email",
    "city",
    "province",
    "postal_code",
    "country",
    "email",
    "latitude",
    "longitude",
    )
CSV_00 = "Node Id #"

@allow_http("POST")
def _import_spreadsheet(request):
    rows = []
    has_errors = False
    
    for key in request.POST.keys():
        if key.startswith("confirm_"):
            counter = key[len("confirm_"):]
            row_data = dict([
                    (i, request.POST["%s_%s" % (i, counter)])
                    for i in CSV_COLUMNS])
            form = SpreadsheetForm(data=row_data)
            if form.is_valid():
                row_data['cleaned_data'] = form.cleaned_data
                rows.append(row_data)
            else:
                has_errors = True
                row_data['errors'] = errors = {}
                errors.update(form.errors)
                rows.append(row_data)

    if has_errors:
        ctx = dict(rows=rows,
                   columns=CSV_COLUMNS)
        return _import_spreadsheet_preview(request, ctx)

    ## DO STUFF NOW

@allow_http("GET", "POST")
@rendered_with("main/import_spreadsheet.html")
def import_spreadsheet(request):
    if request.method == "GET":
        return locals()

    if request.POST.get("confirm", None) == "true":
        return _import_spreadsheet(request)

    data = request.FILES['data']
    data = io.StringIO(data.read().decode("utf8").encode("ascii", "xmlcharrefreplace"), 
                       newline=None)
    
    reader = csv.reader(data)
    lines = [i for i in reader]
    if lines[0][0].strip().lower() == CSV_00.lower():
        lines.pop(0)
    
    rows = []
    lineno = 0
    for line in lines:
        lineno += 1
        try:
            entry = {}
            for i, key in enumerate(CSV_COLUMNS):
                entry[key] = line[i].strip()
            rows.append(entry)
        except IndexError:
            messages.error(request, 'Error reading line %s of the spreadsheet.' % lineno)
            return HttpResponseRedirect(".")

    ctx = dict(rows=rows,
               columns=CSV_COLUMNS)
    return _import_spreadsheet_preview(request, ctx)

@rendered_with("main/import_spreadsheet_preview.html")
def _import_spreadsheet_preview(request, ctx):
    return ctx

@allow_http("GET")
@rendered_with("main/home.html")
def home(request):
    return {}
