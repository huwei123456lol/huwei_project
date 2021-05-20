import connectDatabase

def drop(sql):
	connect = connectDatabase.connect()
	cursor = connect.cursor()
	cursor.execute(sql)
	print("删除成功!")
	cursor.close()
	connect.close()

if __name__ == "__main__":
	#sql = "drop table users;"
	sql = "drop table userinformation;"
	drop(sql)