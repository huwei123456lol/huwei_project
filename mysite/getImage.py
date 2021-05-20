#获取网页图片
header={"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"}
import urllib3
import bs4

poolmanager = urllib3.PoolManager()
response = poolmanager.request(url="https://image.baidu.com/search/index?tn=baiduimage&ct=201326592&lm=-1&cl=2&ie=gb18030&word=%C9%CC%C6%B7%CD%BC%C6%AC%BF%E2&fr=ala&ala=1&alatpl=adress&pos=0&hs=2&xthttps=000000",headers=header,method="GET")
bsoup = bs4.BeautifulSoup(response.data,'lxml')
imgList = bsoup.select('img')
#获得图片路径
"""
img = imgList[0]['src'].split('//')[1]
imgresponse = poolmanager.request(url=img,headers=header,method='GET')
i=1
filename = str(i)+'.'+img.rsplit('.',1)[1]
"""
def getImage():
	i=33
	for img in imgList:
		imgsrc=img['src'].split('//',1)[1]
		filename = str(i)+'.'+imgsrc.rsplit('.',1)[1]
		imgresponse = poolmanager.request(url=imgsrc,headers=header,method='GET')
		with open('static/image/'+filename,'wb+') as f:
			f.write(imgresponse.data)
		i += 1

if __name__ == "__main__":
	"""
	with open('static/image/'+filename,'wb+') as f:
		f.write(imgresponse.data)
		i+=1
	"""
	getImage()