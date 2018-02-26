from django.shortcuts import render
from datetime import datetime
from django.http import HttpResponse, JsonResponse, FileResponse
from django.views.decorators.http import require_http_methods
from django.template import Template, Context
import os


# Create your views here.
@require_http_methods(["GET", "POST"])
def msgproc(request):
    datalist = []
    if request.method == "POST":
        userA = request.POST.get("userA", None)
        userB = request.POST.get("userB", None)
        msg = request.POST.get("msg", None)
        time = datetime.now()
        with open('msgdata.txt', 'a+') as f:
            f.write("{}--{}--{}--{}--\n".format(userB, userA, msg, time.strftime("%Y-%m-%d %H:%M:%S")))
    if request.method == "GET":
        userC = request.GET.get("userC", None)
        if userC is not None:
            with open('msgdata.txt', "r") as f:
                cnt = 0
                for line in f:
                    linedata = line.split('--')
                    print(linedata[0])
                    if linedata[0] == userC:
                        cnt = cnt + 1
                        d = {
                            "userA": linedata[1],
                            "msg": linedata[2],
                            "time": linedata[3]
                        }
                        datalist.append(d)
                    if cnt >= 10:
                        break
    return render(request, "MsgSingleWeb.html", {"data": datalist})


def homeproc(request):
    return HttpResponse(
        "<h2>This is the home page, please visit <a href='./msggate'>Here</a></h2>"
    )


def homeproc1(request):
    response = JsonResponse({'key': 'value1'})
    return response


def homeproc2(request):
    cwd = os.path.dirname(os.path.abspath(__file__))
    response = FileResponse(open(cwd + "/templates/java.jpg", 'rb'))
    response['Content-Type'] = 'application/octet-steam'
    response[
        'Content-Disposition'] = 'attachment;filename="java.jpg"'  # necessary
    return response


def pgproc(request):
    template = Template("<h1>The name of this program is {{ name }}")
    context = Context({"name": "Platform"})
    return HttpResponse(template.render(context))
