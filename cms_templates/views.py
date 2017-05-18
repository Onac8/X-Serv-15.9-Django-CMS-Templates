from django.shortcuts import render
from django.http import *
from django.views.decorators.csrf import csrf_exempt
from cms_templates.models import *
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.template.loader import get_template
from django.template import Context

@csrf_exempt
def home(request):
    if request.user.is_authenticated():
        htmlAnswer = "Logged in as " + request.user.username \
            + ". <a href='/logout'> Logout </a>"

        #pedimos el home
        if request.method == 'GET':
            htmlAnswer = htmlAnswer + "<form id='paginas' method='POST'>" \
                + "<label> Introduce el recurso y el contenido del recurso<br></label>" \
                + "<input name='name' type='text'><br>" \
                + "<textarea name='page' rows='20' cols='100' ></textarea><br>" \
                + "<input type='submit' value='Enviar'></form>"
            list = Pages.objects.all()
            htmlAnswer = htmlAnswer + "Look our pages:<br>"
            for page in list:
                htmlAnswer = htmlAnswer + "<a href='/" + page.nombre \
                    + "'> Page of " + page.nombre + "</a><br>"
            return HttpResponse(htmlAnswer)

        #enviamos form
        elif request.method == 'POST':
            recurso = request.POST['name']
            contenido = request.POST['page']
            pagina = Pages(nombre=recurso, pagina=contenido)
            pagina.save()
            return HttpResponse("POST in /" + recurso)
    else:
        response = HttpResponse()
        response.write("You are not logged in. " \
            + "<a href='/admin/'> Login </a><br> " \
            + "But look our pages: <br>")
        list = Pages.objects.all()
        for page in list:
            response.write("<a href='/" + page.nombre + "'> Page of" + page.nombre + "</a><br>")
        return response

@csrf_exempt

#Podemos entrar a esta view clickeando en uno de los enlaces anteriores o
#poniendo directamente el recurso (/loquesea)
def resource(request, nombreRecurso):
    if request.method == "GET":
        if request.user.is_authenticated():
            htmlAnswer = "Logged in as " + request.user.username \
                + ". <a href='/logout'> Logout </a><br>"
        else:
            htmlAnswer = "You are not logged in. " \
            + "<a href='/admin/'> Login </a><br> "
        try:
            pagina = Pages.objects.get(nombre=nombreRecurso)
            htmlAnswer = htmlAnswer + pagina.pagina
            return HttpResponse(htmlAnswer)
        except Pages.DoesNotExist:
            return HttpResponseNotFound(htmlAnswer + "Page Not Found")
    elif request.method == 'PUT':
        if request.user.is_authenticated:
            try:
                pagina = Pages.objects.get(name=nombreRecurso)
                pagina.page = request.body.decode('utf-8')
                pagina.save()
                return(HttpResponse("Updated resource: /" + nombreRecurso))
            except Pages.DoesNotExist:
                return HttpResponseNotFound("ERROR! Resource doesn't exist!")
        else:
            return HttpResponseBadRequest("ERROR! YOU ARE NOT LOGGED IN. YOU CAN'T PUT")

def logout(request):
    logout(request)
    return redirect(home)


@csrf_exempt
def template(request, recurso):
    if request.user.is_authenticated():
        htmlAnswer = "Logged in as " + request.user.username + ". <a href='/logout'> Logout </a><br>"
    else:
        htmlAnswer = "You are not logged in. <a href='/admin/'> Login </a><br> "

    try:
        pagina = Pages.objects.get(nombre=recurso)
        htmlAnswer = htmlAnswer + pagina.pagina
        return HttpResponse(htmlAnswer)
    except Pages.DoesNotExist:
        return HttpResponseNotFound(htmlAnswer + "Page Not Found")

    template = get_template("index.html")
    c = Context({'title': 'Pagina de ' + recurso, 'content':  pagina.pagina, 'menulogin': htmlAnswer})
    return HttpResponse(template.render(c))
