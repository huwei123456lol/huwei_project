import pymysql
import readInformation

def connect():
	data = readInformation.read()
	return pymysql.Connection(**data)

if __name__ == "__main__":
	print(connect())