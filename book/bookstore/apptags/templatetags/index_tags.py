from django import template

#使用 {% load index_tags %} 加载自定义的标签

register = template.Library()

#注册自定义简单标签
@register.sample_tag
def say_tag(str):
    return "hello" + str

#注册自定义引用标签
@register.inclusion_tag('inclusion.html',takes_context=True)
#定义函数渲染模板文件 inclusion.html
def add_webname_tag(context,namestr): #使用takes_context=True此时第一个参数必须为context
    return {'hello':'%s %s'%(context['varible'],namestr)}

#注册自定义赋值标签
@register.simple_tag
def test_as_tag(strs):
    return 'Hello Test Tag-%s'%strs