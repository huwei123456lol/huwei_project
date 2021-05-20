#插入商店数据库值
import numpy
import flask
import random
import connectDatabase

def insert():
	connect = connectDatabase.connect()
	cursor = connect.cursor()
	for i in numpy.arange(1,25):
		imgUrl="/static/image/"+str(i)+".jpg"
		id = str(i)
		shopname=""
		k=0
		while k <20:
			shopname +=chr(random.randint(65,200))
			k += 1
		price = random.randrange(50,1000)/10
		cursor.execute("insert into shoplist(id,imgSrc,shopname,price) values(%s,%s,%s,%s);",(id,imgUrl,shopname,str(price)))
		connect.commit()
	print('ok')
	cursor.close()
	connect.close()

if __name__ == "__main__":
	insert()
		