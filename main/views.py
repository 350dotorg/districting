from django.contrib import messages
from django.http import (HttpResponse,
                         HttpResponseForbidden, 
                         HttpResponseNotFound)
from django.shortcuts import redirect 
from djangohelpers import (rendered_with,
                           allow_http)

import csv
import io
import json 
import os
import tempfile

from main.forms import SpreadsheetForm
from main.utils import lookup

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

@allow_http("GET")
def download_spreadsheet(request, path):
    path = os.path.join(tempfile.gettempdir(), "districting%s.csv" % path)
    assert os.path.exists(path)
    with open(path) as fp:
        content = fp.read()
    resp = HttpResponse(content, content_type="text/plain")
    resp['Content-Disposition'] = "attachment; filename=districts.csv"
    return resp

@allow_http("POST")
@rendered_with("main/results_summary.html")
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

    try:

        fd, path = tempfile.mkstemp(prefix="districting", suffix=".csv")
        with open(path, 'wb') as fp:
            writer = csv.writer(fp)

            stats = {'federal': {},
                     'state_senate': {},
                     'state_house': {}}

            for row in rows:
                resp = lookup(row['cleaned_data']['latitude'], 
                              row['cleaned_data']['longitude'])
                row['cleaned_data']['districts'] = {
                    'federal': resp[0],
                    'state_senate': resp[1],
                    'state_house': resp[2]
                    }

                if resp[0] not in stats['federal']:
                    stats['federal'][resp[0]] = 0
                stats['federal'][resp[0]] += 1
                if resp[1] not in stats['state_senate']:
                    stats['state_senate'][resp[0]] = 0
                stats['state_senate'][resp[0]] += 1
                if resp[2] not in stats['state_house']:
                    stats['state_house'][resp[2]] = 0
                stats['state_house'][resp[2]] += 1

                data = row['cleaned_data']
                writer.writerow([data['node_id'], 
                                 data['province'],
                                 data['districts']['federal'],
                                 data['districts']['state_senate'],
                                 data['districts']['state_house'],
                                 ])
    except:
        os.unlink(path)
        raise
    prefix = os.path.join(tempfile.gettempdir(), "districting")
    path = path[len(prefix):-4]
    return dict(stats=stats, path=path)

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
            return redirect(".")

    ctx = dict(rows=rows,
               columns=CSV_COLUMNS)
    return _import_spreadsheet_preview(request, ctx)

@rendered_with("main/import_spreadsheet_preview.html")
def _import_spreadsheet_preview(request, ctx):
    return ctx

@allow_http("GET")
@rendered_with("main/home.html")
def home(request):
    return redirect("/upload/")

