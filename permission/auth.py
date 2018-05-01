from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
from MovieBS import settings
class M1(MiddlewareMixin):

    def process_request(self,request):
        if request.path_info == "/login/":
            return None

        is_login = request.session.get(settings.IS_LOGIN)
        if not is_login:
            return redirect('/login/')


    def process_response(self,request,response):
        return response