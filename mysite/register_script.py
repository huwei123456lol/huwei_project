#批量注册脚本
import urllib3
import bs4
import numpy
import random

header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"}
def start():
	poolmanager = urllib3.PoolManager()
	alphaList = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
	for i in numpy.arange(1,10):
		username = alphaList[random.randint(2,24)]+str(123456)+alphaList[i]
		password = alphaList[random.randint(1,10)]+str(123)+alphaList[random.randint(11,20)]+alphaList[random.randint(1,25)]
		name = alphaList[random.randint(1,10)]+alphaList[i]+"hello"
		birthday = "2021-4-9"
		xueli = "大专" if i %2==0 else "本科"
		gender=0 if i %2==0 else 1
		quanxian =0
		response=poolmanager.request(url="http://127.0.0.1:5000/user/register",method="POST",headers=header,fields={"username":username,"password":password,"uname":name,"birthday":birthday,"xueli":xueli,"gender":gender,"user":quanxian})
		bsoup = bs4.BeautifulSoup(response.data,'lxml')
		html = bsoup.select('html')
		print(html)
if __name__ == "__main__":
	start()	