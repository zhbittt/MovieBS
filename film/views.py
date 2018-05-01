from django.shortcuts import render,redirect,HttpResponse
from django.http import JsonResponse
from PIL import Image,ImageDraw,ImageFont
from io import BytesIO
import random
import json

from film.models import *
from .forms import RegForm



import random

def login(request):
    """
    图片点击   登录  login 原始版本
    """
    if request.is_ajax():
        username = request.POST.get("username")
        password = request.POST.get("password")
        validCode = request.POST.get("validCode")
        login_response = {"is_login": False, "error_msg": None}
        if validCode.upper() == request.session.get("keepValidCode").upper():
            userobj=UserInfo.objects.filter(username=username, password=password).first()
            if userobj:
                login_response["is_login"] = True
                request.session["is_login"] = True
            else:
                login_response["error_msg"] = '账号或密码错误'
        else:
            login_response["error_msg"] = '验证码错误'
        return JsonResponse(login_response)
    return render(request, 'login.html')

def logout(request):
    request.session["is_login"] = False
    return redirect("/login/")

def get_validCode_img(request):
    '''
    获取验证码图片
    '''
    img = Image.new(mode="RGB" , size=(120,40) ,color=(random.randint(0,255),random.randint(0,255),random.randint(0,255)))

    draw = ImageDraw.Draw(img,"RGB")
    font = ImageFont.truetype('static/font/kumo.ttf',25)

    valid_list=[]
    for i in range(5):

        random_num =str(random.randint(0,9))
        random_lower_zimu =chr(random.randint(65,90))
        random_upper_zimu = chr(random.randint(97,122))

        random_char = random.choice([random_num,random_lower_zimu,random_upper_zimu])
        draw.text([5+i*24,10],random_char,(random.randint(0,255),random.randint(0,255),random.randint(0,255)),font=font)
        valid_list.append(random_char)

    f = BytesIO()
    img.save(f,'png')
    data = f.getvalue()

    valid_str = "".join(valid_list)
    print(valid_str)

    request.session["keepValidCode"]=valid_str

    return HttpResponse(data)

def reg(request):
    if request.is_ajax():
        form_obj = RegForm(request,request.POST)
        response = {"user":None,"errorList":None}
        if form_obj.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]
            phone = request.POST["phone"]
            head_img = request.FILES["head_img"]
            obj = UserInfo.objects.create(username=username, password=password, phone=phone,head_img=head_img)
            response["user"] = obj.username
        else:
            response["errorList"]=form_obj.errors
        return JsonResponse(response)

    form_obj = RegForm(request)
    return render(request,"reg.html",{"form_obj":form_obj})

def index(request):
    return render(request,"index.html")

def MovieDetail(request):
    return render(request,'detail.html')