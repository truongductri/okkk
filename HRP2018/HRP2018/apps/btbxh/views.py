# from django.http import HttpResponse, HttpResponseRedirect
#
import os
from django.shortcuts import get_object_or_404, render

from django.http import HttpResponse
from django.shortcuts import redirect
import quicky

from . import models
from api.models import auth_user_info
from quicky import applications
from models import Login

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate,login as form_login
import quicky
application=applications.get_app_by_file(__file__)
# from django.urls import reverse
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@quicky.view.template("index.html")
def index(request):
    
    if request.user.is_anonymous():
        return redirect(request.get_app_url("login"))
    else:
        model = {}
        return request.render(model)

def admin(request):
    return render(request, 'admin.html')

@quicky.view.template("login.html")
def login(request):
    #try:
    #    sys_user=User.objects.get(username="sys")
    #except ObjectDoesNotExist as ex:
    #    user = User.objects.create_user('sys', '', '123456')
    #    user.is_active=True
    #    user.is_supperuser=True
    #    user.save()
    _login=models.Login()
    _login.language=request._get_request().get("language","en")
    if request.GET.has_key("next"):
        _login.url_next=request.GET["next"]
        if request._get_post().get("site") != None and request._get_post().get("site") != "":
            _login.url_next= request.GET["next"] + request._get_post().get("site")
    request.session["language"] = _login.language
    if request._get_post().keys().__len__()>0:
        username_request=request._get_post().get("username")
        password_request=request._get_post().get("password")
        try:
            from quicky import tenancy

            user_login = auth_user_info().aggregate().project(username=1, login_account=1)\
                .match("login_account == @account", account = username_request).get_item()
            if user_login==None:
                raise (Exception("User was not found"))

            ret=authenticate(username=user_login['username'], password=password_request,schema=tenancy.get_schema())
            form_login(request,ret,schema=tenancy.get_schema())
            return redirect(request.get_app_url(request._get_post().get("site")))
        except Exception as ex:
            _login.is_error=True
            _login.error_message=request.get_global_res("Username or Password is incorrect")
            return request.render(_login)
    return request.render(_login)

def load_page(request,path):
    try:
        return request.render({})
    except:
        return HttpResponse("page was not found")

@quicky.view.template("sign_out.html")
def sign_out(request):
    membership.sign_out(request.session.session_key)
    request.session.clear()
    return redirect("/")

#@quicky.view.template("list.html")
#def load_list(request,path):
#    #form = getattr(forms, path)
#    return request.render({
#        "path": u"list/" + path.lower()
#    })

@quicky.view.template(
    file="dynamic.html",
    is_public=True
)
def load_page(request,path):
    return  request.render({
        "path":path.lower()
    })

#@quicky.view.template(is_public=True)
#def file_download(request):
#    from api import LMSLS_MaterialManagement as fnMaster
#    id = request.REQUEST['id']
#    if(id != None):
#        data = fnMaster.get_file_by_master_id(str(id))
#        if(data != None):
#            import base64
#            data["files"]["file_data"].decode('base64')
#            from django.http import HttpResponse
#            from wsgiref.util import FileWrapper
        
#            # generate the file
#            res = HttpResponse(data["files"]["file_data"].split(',')[1].decode('base64'))
#            res['Content-Type'] = data["files"]["file_type"]
#            res['Content-Length'] = data["files"]["file_size"]
#            res['Content-Disposition'] = 'attachment; filename=' + data["files"]["file_name"]
#            return res
#        #return response
#    return request