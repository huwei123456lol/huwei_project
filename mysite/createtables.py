#单独通过一个文件创建数据表，提供模板
import connectDatabase

def create(sql):
	connect = connectDatabase.connect()
	cursor = connect.cursor()
	cursor.execute(sql)
	print("恭喜，创建成功!")
	cursor.close()
	connect.close()

if __name__ == "__main__":
	#sql = "create table userinformation(id int(10) auto_increment,name varchar(20) not null,birthday date,xueli varchar(20),gender int(2),primary key(id));"
	#sql = "create table users(id int(10) auto_increment,username varchar(20) not null,password varchar(20) not null,quanxian int(1) default(0),infor_id int(10) not null,primary key(id),foreign key(infor_id) references userinformation(id));"
	sql = "create table shoplist(id int(10) auto_increment,shopname varchar(40) not null,price float(10), imgSrc varchar(40) not null, descr varchar(200),primary key(id));"
	create(sql)

#SQL语句问题