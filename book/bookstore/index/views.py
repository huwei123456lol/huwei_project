from django.shortcuts import render, HttpResponse

# Create your views here.
def test_fun():
    return 'ok'

class test_class:
    def test(self):
        return "you're right!"

def test(request):
    #return HttpResponse("hello world")
    return render(request, 'index/test.html', {"test": "Python语言", "test_fun": test_fun, "test_class": test_class().test})

def test2(request):
    test="python语言"
    return render(request, 'index/test.html', locals())

