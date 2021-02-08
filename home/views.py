import base64
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import xlwt
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from .forms import LoginForm, Department_Form, Pbi_Form
from django.contrib.auth import login, authenticate, logout
from .models import Departments, PBI
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.db.models import Count
import json
from datetime import datetime
import traceback
from django.core.mail import EmailMultiAlternatives, EmailMessage
from kanban.settings import EMAIL_HOST_USER
from django.contrib.auth.decorators import login_required


def index(request):
    try:
        return render(request, "home/index.html")
    except Exception as e:
        trace_back = traceback.format_exc()
        return HttpResponse(str(e) + " " + str(trace_back))


def filter_pbi(request):
    try:
        if request.method == 'GET' and request.is_ajax():
            depart_id = request.GET.get("id", None)
            sprint_value = request.GET.get("drob_box_sprint", None)
            pbi_list_filtered = ""
            if (sprint_value == "null"):
                pbi_list_filtered = PBI.objects.filter(department_id=depart_id)
            if (depart_id == "null"):
                pbi_list_filtered = PBI.objects.filter(sprint=sprint_value)
            if (depart_id != "null" and sprint_value != "null"):
                pbi_list_filtered = PBI.objects.filter(department_id=depart_id, sprint=sprint_value)

        return JsonResponse(pbi_list_for_ajax(pbi_list_filtered), status=200, safe=False)

    except Exception as e:
        trace_back = traceback.format_exc()
        return HttpResponse(str(e) + " " + str(trace_back), status=400)


def update_pbi(request):
    try:
        if request.user.is_authenticated:
            if request.user.is_superuser:
                pbi_list = "";
                if request.method == 'POST' and request.is_ajax():
                    id = request.POST.get("id", None)
                    drop_box_dep_value = request.POST.get("drop_box_dep_value", None)
                    drob_box_sprint_value = request.POST.get("drob_box_sprint_value", None)

                    articles = get_object_or_404(PBI, id=id)
                    form = Pbi_Form(request.POST or None, instance=articles)
                    if form.is_valid():
                        form.save()
                    else:
                        print(form.errors)
                if (drop_box_dep_value != "null" and drob_box_sprint_value == "null"):
                    pbi_list = PBI.objects.filter(department_id=drop_box_dep_value)
                if (drop_box_dep_value == "null" and drob_box_sprint_value != "null"):
                    pbi_list = PBI.objects.filter(sprint=drob_box_sprint_value)
                if (drop_box_dep_value != "null" and drob_box_sprint_value != "null"):
                    pbi_list = PBI.objects.filter(department_id=drop_box_dep_value, sprint=drob_box_sprint_value)
                if (drop_box_dep_value == "null" and drob_box_sprint_value == "null"):
                    pbi_list = PBI.objects.select_related('department').order_by('-id')[:25:1]
                return JsonResponse(pbi_list_for_ajax(pbi_list), status=200, safe=False)
            else:
                return HttpResponse(json.dumps({'bilgi': "1"}),
                                    content_type="application/json")
        else:
            return HttpResponse(json.dumps({'bilgi': "0"}),
                                content_type="application/json")
    except Exception as e:
        trace_back = traceback.format_exc()
        return HttpResponse(str(e) + " " + str(trace_back), status=400)


# @login_required(login_url="login")
def delete_pbi(request):
    try:
        if request.user.is_authenticated:
            if request.user.is_superuser:
                pbi_list = "";
                if request.method == 'GET' and request.is_ajax():
                    drop_box_dep_value = request.GET.get("drop_box_dep_value", None)
                    drob_box_sprint_value = request.GET.get("drop_box_sprint_value", None)
                    delete_id = request.GET.get("id", None)
                    instance = get_object_or_404(PBI, id=delete_id)
                    instance.delete()
                if (drop_box_dep_value != "null" and drob_box_sprint_value == "null"):
                    pbi_list = PBI.objects.filter(department_id=drop_box_dep_value)
                if (drop_box_dep_value == "null" and drob_box_sprint_value != "null"):
                    pbi_list = PBI.objects.filter(sprint=drob_box_sprint_value)
                if (drop_box_dep_value != "null" and drob_box_sprint_value != "null"):
                    pbi_list = PBI.objects.filter(department_id=drop_box_dep_value, sprint=drob_box_sprint_value)
                if (drop_box_dep_value == "null" and drob_box_sprint_value == "null"):
                    pbi_list = PBI.objects.select_related('department').order_by('-id')[:25:1]
                return JsonResponse(pbi_list_for_ajax(pbi_list), status=200, safe=False)
            else:
                return HttpResponse(json.dumps({'bilgi': "0"}),
                                    content_type="application/json")
        else:
            return HttpResponse(json.dumps({'bilgi': "1"}),
                                content_type="application/json")




    except Exception as e:
        trace_back = traceback.format_exc()
        return HttpResponse(str(e) + " " + str(trace_back), status=400)


def pbis(request):
    try:
        form = Pbi_Form(request.POST or None)
        pbi_list = PBI.objects.select_related('department').order_by('-id')[:25:1]
        department_list = Departments.objects.all()
        my_sprint_list = PBI.objects.values('sprint').annotate(Count('sprint'))
        my_sprint_list_new = []
        for i in range(1, 13):
            my_sprint_list_new.append(str(i) + '/' + str(datetime.now().year))

        for db_sprin in my_sprint_list:
            for new_sprint in my_sprint_list_new:
                if db_sprin['sprint'] == new_sprint:
                    my_sprint_list_new.remove(new_sprint)
        context = {
            "form": form,
            "all_pbis": pbi_list,
            "department_list": department_list,
            "my_sprint_list": my_sprint_list,
            "my_sprint_list_new": my_sprint_list_new
        }
        return render(request, "home/pbis.html", context)
    except Exception as e:
        trace_back = traceback.format_exc()
        return HttpResponse(str(e) + " " + str(trace_back))


def loginUser(request):
    try:
        form = LoginForm(request.POST or None)
        context = {
            "form": form
        }
        if request.method == 'POST' and request.is_ajax() and form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is None:
                return HttpResponse(json.dumps({'bilgi': "0"}),
                                    content_type="application/json")
            else:
                login(request, user)
                return HttpResponse(json.dumps({'bilgi': "1"}),
                                    content_type="application/json")

        return render(request, "home/login.html", context)
    except Exception as e:
        trace_back = traceback.format_exc()
        return HttpResponse(str(e) + " " + str(trace_back), status=400)


def logoutuser(request):
    logout(request)
    return redirect("index")


@login_required(login_url="login")
def departments(request):
    try:
        depart = Departments.objects.all()
        return render(request, "home/departments.html", {"departments": depart})
    except Exception as e:
        trace_back = traceback.format_exc()
        return HttpResponse(str(e) + " " + str(trace_back))


def add_departments(request):
    try:
        form = Department_Form(request.POST or None)
        if form.is_valid():
            article = form.save(commit=False)
            article.save()
            return redirect("departments")

        return render(request, "home/add_department.html", {"form": form})
    except Exception as e:
        trace_back = traceback.format_exc()
        return HttpResponse(str(e) + " " + str(trace_back))


def delete_departments(request, id):
    try:
        department = get_object_or_404(Departments, id=id)
        department.delete()
        return redirect("departments")
    except Exception as e:
        trace_back = traceback.format_exc()
        return HttpResponse(str(e) + " " + str(trace_back))


def add_pbi(request):
    try:
        if request.user.is_authenticated:
            form = Pbi_Form(request.POST or None)
            context = {
                "form": form,
            }

            if request.method == 'POST' and request.is_ajax() and form.is_valid():
                article = form.save(commit=False)
                article.save()
                return HttpResponse(json.dumps({'bilgi': "1"}),
                                    content_type="application/json")
            return render(request, "home/add_pbi.html", context)
        else:
            return redirect("login")

    except Exception as e:
        trace_back = traceback.format_exc()
        return HttpResponse(str(e) + " " + str(trace_back), status=400)


def queryset_to_dict(qs, fields=None, exclude=None):
    my_list = []
    for x in qs:
        my_list.append(model_to_dict(x, fields=fields, exclude=exclude))
    return my_list


def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).days)


def filter_report(request):
    try:
        if request.method == 'GET' and request.is_ajax():
            sprint_value = request.GET.get("drob_box_sprint", None)
            all_done_count = PBI.objects.filter(pbi_type="DONE", sprint=sprint_value).count()
            fail_count = 0;
            q_data_for_pie = PBI.objects.filter(pbi_type="DONE", sprint=sprint_value)
            for y in q_data_for_pie:
                a_date = y.actual_date
                f_date = y.finish_date
                dif_date = f_date - a_date
                if dif_date.days < 0:
                    fail_count = fail_count + 1
            if (all_done_count != 0):
                fail_rate = (fail_count / all_done_count) * 100
                succes_rate = 100 - fail_rate
            else:
                fail_rate = 0;
                succes_rate = 0;

            labels = ["succes", "fail"]
            data = [succes_rate, fail_rate]

            q_data_3_day_for_td = PBI.objects.filter(end_day_index=3, pbi_type="TODO", sprint=sprint_value).count()
            q_data_5_day_for_td = PBI.objects.filter(end_day_index=3, pbi_type="INPROGRESS",
                                                     sprint=sprint_value).count()
            # q_data_5_day_for_td=PBI.objects.filter(end_day_index=5).annotate(total=Count('pbi_type')).order_by().count()
            q_data_10_day_for_td = PBI.objects.filter(end_day_index=3, pbi_type="DONE", sprint=sprint_value).count()
            data_bar_3_day = [q_data_3_day_for_td, q_data_5_day_for_td, q_data_10_day_for_td]

            # ------------------------------------------------------------------
            q_data_3_day_for_ip = PBI.objects.filter(end_day_index=5, pbi_type="TODO", sprint=sprint_value).count()
            q_data_5_day_for_ip = PBI.objects.filter(end_day_index=5, pbi_type="INPROGRESS",
                                                     sprint=sprint_value).count()
            q_data_10_day_for_ip = PBI.objects.filter(end_day_index=5, pbi_type="DONE", sprint=sprint_value).count()
            data_bar_5_day = [q_data_3_day_for_ip, q_data_5_day_for_ip, q_data_10_day_for_ip]
            # -----------------------------------------------------------------------
            q_data_3_day_for_done = PBI.objects.filter(end_day_index=10, pbi_type="TODO", sprint=sprint_value).count()
            q_data_5_day_for_done = PBI.objects.filter(end_day_index=10, pbi_type="INPROGRESS",
                                                       sprint=sprint_value).count()
            q_data_10_day_for_done = PBI.objects.filter(end_day_index=10, pbi_type="DONE", sprint=sprint_value).count()
            data_bar_10_day = [q_data_3_day_for_done, q_data_5_day_for_done, q_data_10_day_for_done]
            # -----------------------------------------------------
            department_list = Departments.objects.all()
            list_all_dep_pbi_type = []  # create list
            for depart in department_list:
                list_all_dep_pbi_type.append(
                    {
                        'department': depart.department_name,
                        'todo_count': PBI.objects.filter(department_id=depart.id, pbi_type="TODO",
                                                         sprint=sprint_value).count(),
                        'inporogress_count': PBI.objects.filter(department_id=depart.id, pbi_type="INPROGRESS",
                                                                sprint=sprint_value).count(),
                        'done_count': PBI.objects.filter(department_id=depart.id, pbi_type="DONE",
                                                         sprint=sprint_value).count(),
                    }
                )

            return JsonResponse({
                'labels': labels,
                'data': data,
                'data_bar_3_day': data_bar_3_day,
                'data_bar_5_day': data_bar_5_day,
                'data_bar_10_day': data_bar_10_day,
                "list_all_dep_pbi_type": list_all_dep_pbi_type
            }, status=200, safe=False)
    except Exception as e:
        trace_back = traceback.format_exc()
        return HttpResponse(str(e) + " " + str(trace_back), status=400)


def report(request):
    try:
        all_done_count = q_data_for_pie = PBI.objects.filter(pbi_type="DONE").count()
        fail_count = 0;
        q_data_for_pie = PBI.objects.filter(pbi_type="DONE")
        for y in q_data_for_pie:
            a_date = y.actual_date
            f_date = y.finish_date
            dif_date = f_date - a_date
            if dif_date.days < 0:
                fail_count = fail_count + 1
        if (all_done_count != 0):
            fail_rate = (fail_count / all_done_count) * 100
            succes_rate = 100 - fail_rate
        else:
            fail_rate = 0;
            succes_rate = 0;
        labels = ["succes", "fail"]
        data = [succes_rate, fail_rate]

        q_data_3_day_for_td = PBI.objects.filter(end_day_index=3, pbi_type="TODO").count()
        q_data_5_day_for_td = PBI.objects.filter(end_day_index=3, pbi_type="INPROGRESS").count()
        q_data_10_day_for_td = PBI.objects.filter(end_day_index=3, pbi_type="DONE").count()
        data_bar_3_day = [q_data_3_day_for_td, q_data_5_day_for_td, q_data_10_day_for_td]

        # ------------------------------------------------------------------
        q_data_3_day_for_ip = PBI.objects.filter(end_day_index=5, pbi_type="TODO").count()
        q_data_5_day_for_ip = PBI.objects.filter(end_day_index=5, pbi_type="INPROGRESS").count()
        q_data_10_day_for_ip = PBI.objects.filter(end_day_index=5, pbi_type="DONE").count()
        data_bar_5_day = [q_data_3_day_for_ip, q_data_5_day_for_ip, q_data_10_day_for_ip]
        # -----------------------------------------------------------------------
        q_data_3_day_for_done = PBI.objects.filter(end_day_index=10, pbi_type="TODO").count()
        q_data_5_day_for_done = PBI.objects.filter(end_day_index=10, pbi_type="INPROGRESS").count()
        q_data_10_day_for_done = PBI.objects.filter(end_day_index=10, pbi_type="DONE").count()
        data_bar_10_day = [q_data_3_day_for_done, q_data_5_day_for_done, q_data_10_day_for_done]

        # q_data_5_day_for_td1 = PBI.objects.values('department_id__department_name', 'pbi_type').annotate(total=Count('pbi_type')).order_by(
        #  'department_id')
        department_list = Departments.objects.all()
        list_all_dep_pbi_type = []  # create list
        for depart in department_list:
            list_all_dep_pbi_type.append(
                {
                    'department': depart.department_name,
                    'todo_count': PBI.objects.filter(department_id=depart.id, pbi_type="TODO").count(),
                    'inporogress_count': PBI.objects.filter(department_id=depart.id, pbi_type="INPROGRESS").count(),
                    'done_count': PBI.objects.filter(department_id=depart.id, pbi_type="DONE").count(),
                }
            )

        my_sprint_list = PBI.objects.values('sprint').annotate(Count('sprint'))
        return render(request, 'home/report.html', {
            'labels': labels,
            'data': data,
            'data_bar_3_day': data_bar_3_day,
            'data_bar_5_day': data_bar_5_day,
            'data_bar_10_day': data_bar_10_day,
            "my_sprint_list": my_sprint_list,
            "list_all_dep_pbi_type": list_all_dep_pbi_type
        })
    except Exception as e:
        trace_back = traceback.format_exc()
        return HttpResponse(str(e) + " " + str(trace_back))


def export_to_excel(request):
    try:
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="Kanban_Export.xls"'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Kanban')
        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        columns = ['Id', 'Department', 'Sprint', 'Type', 'PBI', 'Classification', 'Workorder Date', 'Start Date',
                   'Finish Date', 'Actual Date']

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        # Sheet body, remaining rows
        rows = "";
        if request.method == 'GET' and request.is_ajax():
            sprint_value = request.GET.get("drob_box_sprint_value", None)
            if sprint_value != "null":
                rows = PBI.objects.filter(sprint=sprint_value).values_list('id', 'department_id__department_name',
                                                                           'sprint',
                                                                           'pbi_type', 'pbi', 'classficition',
                                                                           'workorder_date', 'start_date',
                                                                           'finish_date',
                                                                           'actual_date')
            else:
                rows = PBI.objects.all().values_list('id', 'department_id__department_name', 'sprint',
                                                     'pbi_type', 'pbi', 'classficition',
                                                     'workorder_date', 'start_date', 'finish_date',
                                                     'actual_date')

        font_style = xlwt.XFStyle()
        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)

        wb.save(response)

        return response
    except Exception as e:
        trace_back = traceback.format_exc()
        return HttpResponse(str(e) + " " + str(trace_back), status=400)


def sprint_gecisi(request):
    try:
        my_sprint_list = PBI.objects.values('sprint').annotate(Count('sprint'))
        my_sprint_list_new = []
        for i in range(1, 13):
            my_sprint_list_new.append(str(i) + '/' + str(datetime.now().year))

        for db_sprin in my_sprint_list:
            for new_sprint in my_sprint_list_new:
                if db_sprin['sprint'] == new_sprint:
                    my_sprint_list_new.remove(new_sprint)

        context = {
            "my_sprint_list": my_sprint_list,
            "my_sprint_list_new": my_sprint_list_new
        }
        return render(request, "home/sprint_gecisi.html", context)
    except Exception as e:
        trace_back = traceback.format_exc()
        return HttpResponse(str(e) + " " + str(trace_back), status=400)

def sprint_gecisi_done(request):
    try:
        if request.user.is_authenticated:
            if request.user.is_superuser:
                if request.method == 'GET' and request.is_ajax():
                    sprint_value = request.GET.get("drob_box_sprint_value", None)
                    drob_box_new_sprint_value = request.GET.get("drob_box_new_sprint_value", None)
                    if (sprint_value != "null"):
                        pbi_list_filtered = PBI.objects.filter(sprint=sprint_value).exclude(pbi_type="DONE")
                        for pbi in pbi_list_filtered:
                            pbi.sprint = drob_box_new_sprint_value
                        for pbi in pbi_list_filtered:
                            PBI(department=pbi.department,
                                sprint=drob_box_new_sprint_value,
                                end_day_index=pbi.end_day_index,
                                pbi_type=pbi.pbi_type,
                                pbi=pbi.pbi,
                                classficition=pbi.classficition,
                                workorder_date=pbi.workorder_date,
                                start_date=pbi.start_date,
                                finish_date=pbi.finish_date,
                                actual_date=pbi.actual_date
                                ).save()
                    # print(queryset_to_dict(pbi_list_filtered))

                    return HttpResponse(json.dumps({'bilgi': "1"}),
                                        content_type="application/json")
            else:
                return HttpResponse(json.dumps({'bilgi': "2"}),
                                    content_type="application/json")

        else:
            return HttpResponse(json.dumps({'bilgi': "0"}),
                                content_type="application/json")
    except Exception as e:
        trace_back = traceback.format_exc()
        return HttpResponse(str(e) + " " + str(trace_back), status=400)


def send_mail_content(request):
    try:
        if request.user.is_authenticated:
            if request.user.is_superuser:
                if request.method == 'GET' and request.is_ajax():
                    base64date_for_bar = request.GET.get("base_64_for_bar", None).replace(" ", "+")
                    base64date_for_pie = request.GET.get("base_64_for_pie", None).replace(" ", "+")
                    sprint_value = request.GET.get("drob_box_sprint", None)
                    department_list = Departments.objects.all()
                    list_all_dep_pbi_type = []  # create list

                    if sprint_value != "null":
                        for depart in department_list:
                            list_all_dep_pbi_type.append(
                                {
                                    'department': depart.department_name,
                                    'todo_count': PBI.objects.filter(department_id=depart.id, pbi_type="TODO",
                                                                     sprint=sprint_value).count(),
                                    'inporogress_count': PBI.objects.filter(department_id=depart.id,
                                                                            pbi_type="INPROGRESS",
                                                                            sprint=sprint_value).count(),
                                    'done_count': PBI.objects.filter(department_id=depart.id, pbi_type="DONE",
                                                                     sprint=sprint_value).count(),
                                }
                            )
                    else:
                        for depart in department_list:
                            list_all_dep_pbi_type.append(
                                {
                                    'department': depart.department_name,
                                    'todo_count': PBI.objects.filter(department_id=depart.id, pbi_type="TODO").count(),
                                    'inporogress_count': PBI.objects.filter(department_id=depart.id,
                                                                            pbi_type="INPROGRESS").count(),
                                    'done_count': PBI.objects.filter(department_id=depart.id, pbi_type="DONE", ).count()

                                })
                    string_rows_and_columun = "";
                    for depart in list_all_dep_pbi_type:
                        string_rows_and_columun += "<tr>"
                        string_rows_and_columun += "<td>"
                        string_rows_and_columun += depart['department']
                        string_rows_and_columun += "</td>"
                        string_rows_and_columun += "<td>"
                        string_rows_and_columun += str(depart['todo_count'])
                        string_rows_and_columun += "</td>"
                        string_rows_and_columun += "<td>"
                        string_rows_and_columun += str(depart['inporogress_count'])
                        string_rows_and_columun += "</td>"
                        string_rows_and_columun += "<td>"
                        string_rows_and_columun += str(depart['done_count'])
                        string_rows_and_columun += "</td>"
                        string_rows_and_columun += "</tr>"
                    # image is User's model field
                    # if len(sprint_value) % 4:
                    #      sprint_value += '=' * (4 - len(sprint_value) % 4)
                subject = "bekir"
                to = 'alattin.ozdemir@vodafone.com'

                html_part = MIMEMultipart(_subtype='related')
                body = MIMEText(' <style>'

                                ' table {'
                                'border: 1px solid gray;'
                                '}'
                                'td {'
                                'border: 1px solid gray;'
                                'height: 20px;'
                                'width: 142px;'
                                'text-align: center; '
                                'font-family:arial;'
                                'font-size: 12px;'
                                '}'
                                'th {'
                                'border: 1px solid gray;'
                                'font-family:arial;'
                                '}'
                                '</style>'
                                '<p style="font-size:13px; font-family:Trebuchet MS, Arial, Helvetica, sans-serif">'
                                'Merhabalar<br><br>&nbsp; &nbsp; &nbsp;Bölgelere ait 0.5 ve üstü pocket loss durumu aşağıdaki gibidir. İllere ait pocket loss meydana gelen sahalar ekte sunulmuştur.<br><br> </p>'
                                '<img src="cid:myimage1" /> '
                                '<br>'
                                '<img src="cid:myimage" /><br>'
                                "<table cellpadding='0' cellspacing='0'>  "
                                "<thead>"
                                "<tr>"
                                "<th>Department</th>"
                                "<th>TODO</th>"
                                "<th>INPROGRESS</th>"
                                "<th>DONE</th>"
                                "</tr>"
                                "</thead>"
                                "<tbody>" + string_rows_and_columun +
                                "</tbody>"
                                "</table>",
                                _subtype='html')
                html_part.attach(body)
                img = MIMEImage(base64.decodebytes(base64date_for_bar.encode()), 'png')
                img.add_header('Content-Id', '<myimage>')  # angle brackets are important
                img.add_header("Content-Disposition", "inline", filename="myimage")  # David Hess recommended this edit
                img1 = MIMEImage(base64.decodebytes(base64date_for_pie.encode()), 'jpeg')
                img1.add_header('Content-Id', '<myimage1>')  # angle brackets are important
                img1.add_header("Content-Disposition", "inline",
                                filename="myimage1")  # David Hess recommended this edit

                html_part.attach(img)
                html_part.attach(img1)
                msg = EmailMessage(subject, "aladdim", EMAIL_HOST_USER, [to])
                msg.attach(html_part)
                msg.send()

                return HttpResponse(json.dumps({'bilgi': "1"}),
                                    content_type="application/json")
            else:
                return HttpResponse(json.dumps({'bilgi': "2"}),
                                    content_type="application/json")

        else:
            return HttpResponse(json.dumps({'bilgi': "0"}),
                                content_type="application/json")
    except Exception as e:
        trace_back = traceback.format_exc()
        return HttpResponse(str(e) + " " + str(trace_back), status=400)


def pbi_list_for_ajax(qs):
    list_all = []  # create list
    for x in qs:
        list_all.append({'department': x.department.department_name,
                         'sprint': x.sprint,
                         'end_day_index': x.end_day_index,
                         'pbi_type': x.pbi_type,
                         'pbi': x.pbi,
                         'classficition': x.classficition,
                         'workorder_date': x.workorder_date,
                         'start_date': x.start_date,
                         'finish_date': x.finish_date,
                         'actual_date': x.actual_date,
                         'id': x.id

                         })
    return list_all
# print(list_all)
