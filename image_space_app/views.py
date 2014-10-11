from django.http import HttpResponse
from django.template import RequestContext, loader
from django.contrib import auth
from django.shortcuts import render_to_response,redirect
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout




def index(request):
    template = loader.get_template('image_space_app/index.html')
    context = RequestContext(request, {})
    return HttpResponse(template.render(context))
def sign_up(request):
    template = loader.get_template('image_space_app/sign_up.html')
    context = RequestContext(request, {})
    return HttpResponse(template.render(context))
def login_user(request):
    logout(request)
    username = password = ''
    if request.POST:
        username = request.POST['email']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/index/')
    return render_to_response('image_space_app/login.html', context_instance=RequestContext(request))

