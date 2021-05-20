import json

def read():
	data = None
	with open("databaseInformation.txt","r+",encoding="utf-8") as f:
		data = f.read()
	#验证是否读取到信息
	if data:
		#查看最后一行是否含有标点符号
		newData = data.replace(";",",")
		if newData.endswith(','):
			tempData = '{'+newData.rsplit(',',1)[0]+'}'
			return json.loads(tempData)
		return json.loads('{'+newData+'}')
		


if __name__ == "__main__":
	print(read())