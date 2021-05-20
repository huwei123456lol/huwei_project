#这个文件主要用于复习一下装饰器的使用
def wrap(func):
	def base():
		print("hello")
		func()
		print("word")
	return base

@wrap
def say():
	print("+")

if __name__ == "__main__":
	say()