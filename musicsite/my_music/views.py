from django.shortcuts import render, HttpResponse, redirect
from . import models
import time
import bs4
import urllib3
import re
import urllib.parse as parse
import base64
import random
import os
# Create your views here.


def login(request):     # 登陆
    return render(request, 'login.html')


def checkuser(request):     # 检查用户是否存在或者
    if request.method == 'POST' and request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = models.User.objects.get(username=username)
            if password == user.password:
                request.session['user'] = username
                request.session['img'] = str(user.img)
                return redirect('../user/index')   # 登陆成功后返回首页
            else:
                return HttpResponse('password error')
        except:
            return HttpResponse('user error')

def mymusic(request):
    #登陆后的首页
    username = request.session.get('user')
    img = request.session.get('img')
    # 获取username的所有歌曲
    music_list = []
    user = models.User.objects.get(username=username)
    userInfo = models.UserInfo.objects.get(id=user.userInfo_id)
    user_id = user.id
    musics = models.Music.objects.filter(user_id=user_id)
    if not musics:
        music_list.append("你还没有歌曲呐，请添加")
    else:
        for item in musics:
            music_list.append(item.geming)
    # 传送数据
    data = {'user': userInfo.name, 'img': img, 'ge_ming': music_list}
    return render(request, 'userindex.html', {'data': data})

def myregister(request):
    return render(request, 'register.html')

def register(request):  # 注册，先注册userInfo,再user
    if request.method == 'POST' and request.POST:
        name = request.POST.get('name')
        sex = request.POST.get('sex')
        birthday = request.POST.get('birthday')
        ai_hao = request.POST.get('aihao')
        username = request.POST.get('username')
        password = request.POST.get('password')
        last_login_in = time.strftime('%Y-%m-%d')
        myimg = request.POST.get('myImg')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        # 查询是否存在username and name
        test_user = models.User.objects.filter(username=username)
        test_userinfo = models.UserInfo.objects.filter(name=name)
        if test_user:
            return HttpResponse('用户名已存在,请重新注册')
        if test_userinfo:
            return HttpResponse('你的名字已存在，请重新注册')
        userInfo = models.UserInfo(name=name, sex=sex, birthday=birthday, email=email, ai_hao=ai_hao, phone=phone)
        userInfo.save()
        user = models.User(username=username, password=password, last_login_in=last_login_in, img=myimg,
                           userInfo=userInfo)
        user.save()
        return HttpResponse('注册成功')


def my_music_list(request):     # 查找我的音乐
    if request.method == 'POST' and request.POST:
        username = request.POST.get('username')
        if username is None or username == "":
            return HttpResponse({'error': '请登录'})
        else:
            username = request.POST.get('username')
            try:
                user = models.User.objects.get(username=username)
                music_list = models.Music.objects.get(user=user)
                return HttpResponse(music_list)
            except Exception as e:
                with open('../errlog.txt', 'w+', encoding='utf-8') as err_log:
                    err_log.write(e)
                    err_log.close()
    return render(request, 'login.html')

# js 验证用户不为空
def get_connect_prepare(request):
    if request.method == "POST" and request.POST:
        info = request.POST.get('info')  # 获得用户信息
        username = info.get('username')
        password = info.get('password')
        try:
            pwd = models.User.objects.get(username=username)
            if password == pwd:
                request.session['info'] = {
                    'username': username,
                    'password': password
                }
                return redirect('../chat')
            else:
                return HttpResponse('密码错误')
        except:
            return HttpResponse('用户名错误')


def searchByValue(request):
    urllib3.disable_warnings()
    ge_ming_list = []
    if request.method == "POST" and request.POST:
        ge_ming = request.POST.get('ge_ming')
        url = "https://www.90lrc.cn"
        use_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                    'Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3823.400 QQBrowser/10.7.4307.400'
        accept_language = 'zh-CN,zh;q=0.9'
        accept_encoding = 'gzip, deflate, br'
        headers = {'user-agent': use_agent, 'accept-language': accept_language, 'accept-encoding': accept_encoding}
        poolroom = urllib3.PoolManager()
        context = poolroom.request(url=url + '/so.php?wd={}'.format(parse.quote(ge_ming)),
                                   method='get', headers=headers).data.decode('utf-8')
        beautiful = bs4.BeautifulSoup(context, 'lxml')
        ul_list = beautiful.find_all('ul')
        ge_ci_url = set()
        for item in ul_list:
            a_list = item.find_all('a')
            for a in a_list:
                if re.match(r'^/geci', a['href']):
                    ge_ci_url.add(a['href'])
        for temp in ge_ci_url:
            temp_url = url + temp
            ge_ci_body = poolroom.request(url=temp_url, method='get', headers=headers).data.decode('utf-8')
            soup = bs4.BeautifulSoup(ge_ci_body, 'lxml')
            p_list = soup.find_all('p')
            for p in p_list:
                if p['id'] == 'txt':
                    ge_ming_list.append(p.next.strip())
        ge_ming_str = ",".join(ge_ming_list)
        return HttpResponse(ge_ming_str)

def findValue(request):
    if request.method == "POST" and request.POST:
        ge_ming = request.POST.get('ge_ming')
        request.session['username'] = request.POST.get('username')
        request.session['img'] = request.POST.get('img')
        try:
            music = models.Music.objects.get(geming=ge_ming)
            request.session['ge_ci'] = music.gechi
            print(music.gechi)
            return redirect('../sing')
        except:
            #   内部数据库没有查到数据时条用外部数据库
            request.session['ge_ming'] = ge_ming
            return redirect('../../../temp')

def sing(request):
    img = request.session.get('img')
    username = request.session.get('username')
    ge_ci = request.session.get('ge_ci').split("\n")

    data = {'img': img, 'username': username, 'ge_ci': ge_ci}
    return render(request, 'usersing.html', {'data': data})

def myUserInfo(request):
    if request.method == "POST" and request.POST:
        username = request.POST.get('username')
        userInfo = models.UserInfo.objects.get(name=username)
        id = userInfo.id
        sex = userInfo.sex
        birthday = userInfo.birthday
        email = userInfo.email
        phone = userInfo.phone
        ai_hao = userInfo.ai_hao
        request.session['id'] = id
        request.session['name'] = username
        request.session['sex'] = sex
        request.session['birthday'] = birthday
        request.session['email'] = email
        request.session['phone'] = phone
        request.session['ai_hao'] = ai_hao
        return redirect('../user/displayInfo')


def displayMyInfo(request):
    id = request.session.get('id')
    username = request.session.get('name')
    sex = request.session.get('sex')
    birthday = request.session.get('birthday')
    email = request.session.get('email')
    phone = request.session.get('phone')
    ai_hao = request.session.get('ai_hao')
    data = {"id": id, "name": username, "sex": sex, "birthday": birthday, "email": email, "phone": phone, "ai_hao": ai_hao}
    return render(request, "userinfo.html", {'data': data})

def updateMyInfo(request):
    if request.method == 'POST' and request.POST:
        id = request.POST.get('id')
        name = request.POST.get('name')
        sex = request.POST.get('sex')
        birthday = request.POST.get('birthday')
        ai_hao = request.POST.get('aihao')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        userInfo = models.UserInfo(id=id, name=name, sex=sex, birthday=birthday, email=email, ai_hao=ai_hao, phone=phone)
        userInfo.save()
        return HttpResponse("更新成功")

def acceptImg(request):
    if request.method == 'POST':
        img = request.POST.get('img')   # 包含图片样式和图片代码的字符串，中间用","分隔，所以需要使用split
        img_data = base64.b64decode(img.split(",")[1])
        imgdir = str(random.randint(5, 100))+".jpg"
        basedir = os.path.join(os.getcwd(), os.path.join("static", "tmpimg"))
        file = os.path.join(basedir, imgdir)
        touchfile(file, img_data)
        return HttpResponse(imgdir)

def touchfile(file, data):
    if file is not exit:
        with open(file, 'wb+') as f:
            f.write(data)
            f.close()
