from django.shortcuts import render, HttpResponse, redirect
from . import  models
import bs4
import urllib3
import re
import urllib.parse as parse
import chardet
# Create your views here.


# 从数据库中获取，如果数据库没有就下载
def download_default_ge_ming(request):
    ge_name_list = set()
    result = models.DefaultMusic.objects.filter()
    if result:
        for item in result:
            ge_name_list.add(item.music_name)
        return render(request, 'index.html', {'ge_ming': ge_name_list})
    urllib3.disable_warnings()
    url = "https://www.90lrc.cn"
    use_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                'Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3823.400 QQBrowser/10.7.4307.400'
    accept_language = 'zh-CN,zh;q=0.9'
    accept_encoding = 'gzip, deflate, br'
    headers = {'user-agent': use_agent, 'accept-language': accept_language, 'accept-encoding': accept_encoding}
    poolroom = urllib3.PoolManager()
    content = poolroom.request(url=url, method='get', headers=headers)
    download_data = content.data.decode('utf-8')
    ge_ci_url = set()
    ge_shou_url = set()
    beautifully = bs4.BeautifulSoup(download_data, 'lxml')
    find_a_list = beautifully.find_all('a')
    for a in find_a_list:
        temp_url = a['href']
        if re.match(r'^/geshou', temp_url):
            ge_shou_url.add(temp_url)
        if re.match(r'^/geci', temp_url):
            ge_ci_url.add(temp_url)
    # 通过歌手url找到歌词url
    for ge_shou_url_temp in ge_shou_url:
        ge_shou_url_temp = url + ge_shou_url_temp
        ge_shou_url_content = poolroom.request(url=ge_shou_url_temp, method='get', headers=headers)
        bSoup = bs4.BeautifulSoup(ge_shou_url_content, 'lxml')
        # 找到路径
        a_list = bSoup.find_all('a')
        for a in a_list:
            if re.match(r'^/geci', a['href']):
                ge_ci_url.add(a['href'])
    # 找到歌词
    ge_ci_body_list = []
    for item in ge_ci_url:
        ge_ci_url_temp = url+item   # 歌词的全路径
        ge_ci_body = poolroom.request(url=ge_ci_url_temp, method='get', headers=headers)
        text = ge_ci_body.data.decode('utf-8')
        bs = bs4.BeautifulSoup(text, 'lxml')
        p_text = bs.find_all('p')
        if p_text:
            for p_id in p_text:
                if p_id['id'] == 'txt':
                    ge_ci_body_list.append(p_id)
    # 每个歌词里面有一些夹带，需要删除。先存入数据库
    for temp_item in ge_ci_body_list:
        name = temp_item.next.strip()
        ge_name_list.add(name)
        author = temp_item.next.next.next.strip()
        try:
            obj = models.Author(author_name=author)
            obj.save()
            music = models.DefaultMusic(music_name=name, music_ge_chi=temp_item.text, music_author=obj)
            music.save()
        except:
            return render(request, 'index.html', {'ge_ming': ['exception']})
    # 返回歌名
    return render(request, 'index.html', {'ge_ming': ge_name_list})
    #return HttpResponse({'ge_name': ge_name_list})


# 导航栏搜索查看数据库里面是否有这首歌，如果没有就下载并返回歌单
def find_by_ge_ming(request):
    urllib3.disable_warnings()
    ge_ming_list = []
    if request.method == 'POST' and request.POST:
        ge_ming = request.POST.get('ge_ming')
        search_musics = models.DefaultMusic.objects.filter(music_name=ge_ming)
        if search_musics:
            for item in search_musics:
                ge_ming_list.append(item.music_name)
            request.session['ge_ming'] = ge_ming_list
            return redirect('../display')
        else:
            url = "https://www.90lrc.cn"
            use_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                        'Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3823.400 QQBrowser/10.7.4307.400'
            accept_language = 'zh-CN,zh;q=0.9'
            accept_encoding = 'gzip, deflate, br'
            headers = {'user-agent': use_agent, 'accept-language': accept_language, 'accept-encoding': accept_encoding}
            poolroom = urllib3.PoolManager()
            context = poolroom.request(url=url+'/so.php?wd={}'.format(parse.quote(ge_ming)),
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
                temp_url = url+temp
                ge_ci_body = poolroom.request(url=temp_url, method='get', headers=headers).data.decode('utf-8')
                soup = bs4.BeautifulSoup(ge_ci_body, 'lxml')
                p_list = soup.find_all('p')
                for p in p_list:
                    if p['id'] == 'txt':
                        ge_ming_list.append(p.next.strip())
                        try:
                            author = models.Author(author_name=p.next.next.next.strip())
                            author.save()
                            music = models.DefaultMusic(music_name=p.next.strip(), music_ge_chi=p.text.strip(),
                                                        music_author=author)
                            music.save()
                        except:
                            continue
            request.session['ge_ming'] = ge_ming_list
            return redirect('../display')

# 显示歌名列表
def display_ge_ming(request):
    ge_ming_list = request.session.get('ge_ming')
    return render(request, 'display_ge_ming.html', {'ge_ming': ge_ming_list})

#   通过歌名找到歌词
def search_by_ge_ming(request):
    if request.method == 'POST' and request.POST:
        ge_ming = request.POST.get('ge_ming')
        try:
            music = models.DefaultMusic.objects.get(music_name=ge_ming)
            request.session['ge_ci'] = music.music_ge_chi
            request.session['ge_ming'] = ge_ming
            return redirect('../display/ge_ci')
        except:
            request.session['ge_ci'] = None
            request.session['ge_ming'] = ge_ming
            return redirect('../display/ge_ci')

# 显示歌词
def display_ge_ci(request):
    ge_ci = request.session.get('ge_ci').split("\n")
    ge_ming = request.session.get('ge_ming')
    if ge_ci is None:
        data = {'ge_ming': ge_ming, 'ge_ci': 'error'}
        return render(request, 'default_sing.html', {'data': data})
    else:
        data = {'ge_ming': ge_ming, 'ge_ci': ge_ci}
        return render(request, 'default_sing.html', {'data': data})

def test(request):
    return render(request, 'test.html')


def test_redirect(request):
    ge_ci = request.session.get('ge_ci')
    if not ge_ci:
        ge_ming_list = request.session.get('ge_ming_list')
        return render(request, 'test2.html', {'ge_ming': ge_ming_list})
    return render(request, 'test2.html', {'ge_ci': ge_ci})


# 自定义去掉歌词的各种填充
def check_ge_ci(ge_ci):
    pass
#  自己开始写网页模板吧

# 返回数据库中的歌名
def get_ge_ming(request):
    ge_ming_list = set()
    result = models.DefaultMusic.objects.filter()
    for item in result:
        ge_ming_list.add(item.music_name)
    ge_ming = ",".join(ge_ming_list)
    return HttpResponse(ge_ming)


def get_ge_ci(request):
    ge_ming = request.session.get('ge_ming')
    # 通过搜索栏搜索到的歌名在本地数据库中没有
    try:
        music = models.DefaultMusic.objects.get(music_name=ge_ming)
        ge_ci = music.music_ge_chi
        request.session['ge_ci'] = ge_ci
        return redirect('../my_music/user/sing')
    except:
        request.session['ge_ci'] = "数据出错，抱歉我的小主人。请重新查找"
        return redirect('../my_music/user/sing')
