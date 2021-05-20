import flask
import connectDatabase
import random
import numpy
import createtables
from sklearn.feature_extraction  import text
import jieba
from sklearn import naive_bayes
#from sklearn import pipeline
#from sklearn import preprocessing
#from sklearn import ensemble
#from sklearn import multioutput
#from sklearn import neural_network
from sklearn import cluster

numpy.random.seed(0)

def getData(filename):
	with open(filename,'r+',encoding='utf-8') as f:
		data=f.read()
	temp_data=data.split('\n')
	questions=[]
	answers=[]
	for temp in temp_data:
		questions.append("".join(jieba.lcut(temp.split(',')[0])))
		answers.append("".join(jieba.lcut(temp.split(',')[1])))
	count_vet=text.CountVectorizer(min_df=1,max_df=20,analyzer='char')
	X=count_vet.fit_transform(questions).toarray()
	y=count_vet.fit_transform(answers).toarray()
	answer_vocabulary=count_vet.get_feature_names()
	with open('data/question.txt','w+',encoding='utf-8') as f:
		for question in questions:
			f.write(question+'\n')
	with open('data/answer.txt','w+',encoding='utf-8') as f:
		for answer in answers:
			f.write(answer+'\n')
	i=0
	while i<len(X):
		j=0
		while j<len(X[0]):
			if X[i][j]>0:
				X[i][j]=j
			else:
				X[i][j]=-1
			j+=1
		i+=1
	m=0
	while m<len(y):
		n=0
		while n<len(y[0]):
			if y[m][n]>0:
				y[m][n]=n
			else:
				y[m][n]=-1
			n+=1
		m+=1
	lens=len(X[0])
	return X,y,lens,answer_vocabulary
	
def data_train(X,y,lens):
	'''	mc=neural_network.MLPClassifier(hidden_layer_sizes=(100,40),max_iter=5000,random_state=0)
	knn=multioutput.MultiOutputRegressor(mc)
	knn.fit(X,y)
	'''
	knn=cluster.KMeans(n_clusters=30).fit(X,y)
	return knn

app = flask.Flask(__name__)
app.secret_key = "jiamisession"

"""
早期使用
def getImage():
	imgList = []
	for i in numpy.arange(1,25):
		imgUrl = flask.url_for('static',filename='image/'+str(i)+ '.png')
		imgList.append(imgUrl)
	return imgList
"""

idList =[]
sysvalue={'bg':"00",'bgmusic':'10','transparency':'22','fontsize':'30','fontcolor':'40'}
def getsystemvalue():
	try:
		systemvalue = flask.session['system']
	except:
		systemvalue = sysvalue
	return systemvalue

@app.route('/')
@app.route('/<username>')
def index(username=None):
	#imglist = getImage()
	connect = connectDatabase.connect()
	cursor = connect.cursor()
	try:
		systemvalue = getsystemvalue()
		cursor.execute('select id,imgSrc,shopname from shoplist;')
		shopValue = cursor.fetchall()
		return flask.render_template('index.html',username=username,shopValue=shopValue,systemvalue=systemvalue)
	except:
		return "数据异常，请刷新重试！"
	finally:
		cursor.close()
		connect.close()

@app.route('/shop/play',methods=["GET","POST"])
def shopplay():
	systemvalue=getsystemvalue()
	if flask.request.method == "POST":
		#展示商品
		id= flask.request.form.get('id')
		connect = connectDatabase.connect()
		cursor = connect.cursor()
		try:
			cursor.execute('select imgSrc,shopname,descr,price  from shoplist where id=%s;',(id))
			shopvalue = cursor.fetchall()
			#存储商品id
			flask.session['id'] = id
			#存储临时商品信息
			flask.session['tempShopInformation'] = shopvalue
			return 'ok'
		except:
			return 'error'
		finally:
			cursor.close()
			connect.close()
	return flask.render_template('shopplay.html',shopValue=flask.session['tempShopInformation'],systemvalue=systemvalue)

@app.route('/shop/shoplist')
def shoplist():
	#判断是否用户登录
	try:
		user = flask.session['username']	
		id = flask.session['id']
		idList.append(id)
		return user
	except:
		return 'error'

@app.route('/shop/noShopList')
def displaynoshoplist():
	try:
		username = flask.session['username']
	except:
		username=None
	return flask.render_template('noShopList.html',username=username)	

@app.route('/shop/shoplist/lookup',methods=['GET','POST'])
def lookupShopList():
	systemvalue=getsystemvalue()
	if flask.request.method == 'POST':
		try:
			sql = "select shopname,descr,price from shoplist where id={};"
			tempsql = "  or id=" .join(idList)
			connect = connectDatabase.connect()
			cursor = connect.cursor()
			try:
				cursor.execute(sql.format(tempsql))
				shopvalueList = cursor.fetchall()
				flask.session['shopvalueList'] = shopvalueList
				return 'ok'	 
			except:
				return "dataerror"
		except:
			return 'error'
	shopvalue = flask.session['shopvalueList']
	try:
		user = flask.session['username']
	except:
		user = None
	return flask.render_template('shoplist.html',shopvalue=shopvalue,user=user,systemvalue=systemvalue)

@app.route('/shop/index')
def returnIndex():
	try:
		user = flask.session['username']
		return user
	except:
		return 'error'

@app.route('/shop/result')
def result():
	systemvalue=getsystemvalue()
	id = flask.session['id']
	connect = connectDatabase.connect()
	cursor = connect.cursor()
	try:
		user=flask.session['username']
	except:
		user = None
	try:
		cursor.execute('select shopname,imgSrc,price from shoplist where id=%s;',(id))
		shopvalue = cursor.fetchall()
		return flask.render_template('result.html',shopValue=shopvalue,systemvalue=systemvalue,user=user)
	except:
		return "服务异常,请刷新重试！"
	finally:
		cursor.close()
		connect.close()

@app.route('/admin/')
@app.route('/admin/<username>')
def admin(username=None):
	if username == None:
		username = flask.session['username']
	connect = connectDatabase.connect()
	cursor = connect.cursor()
	try:
		cursor.execute('show tables;')
		tables = cursor.fetchall()
		connect.commit()
		try:
			cursor.execute("select username from users;")
			users = cursor.fetchall()
			connect.commit()
			return flask.render_template('admin.html',tables=tables,users=users,username=username)
		except:
			connect.rollback()
			return "暂时没有数据哦"
	except:
		connect.rollback()
		return "数据异常!"
	finally:
		cursor.close()
		connect.close()

@app.route('/admin/table/look',methods=["POST","GET"])
def looktable():
	if flask.request.method == "POST":
		tablename = flask.request.form.get('tablename')
		connect = connectDatabase.connect()
		cursor = connect.cursor()
		sql = "desc "+tablename+";"
		try:
			cursor.execute(sql)	
			revalue = cursor.fetchall()
			#(('id', 'int(2)', 'NO', 'PRI', None, ''),
			# ('imgUrl', 'varchar(20)', 'NO', '', None, ''), 
			#('descr', 'varchar(100)', 'YES', '', None, ''),
			# ('price', 'float', 'YES', '', None, ''))
			flask.session["tableAttr"] = revalue
			flask.session['tablename'] = tablename
			return 'ok'
		except:
			return "数据表名异常"
		finally:
			cursor.close()
			connect.close()
	return flask.render_template('looktable.html',tablename=flask.session['tablename'],tableattr=flask.session['tableAttr'])

@app.route('/admin/table/data/add',methods=['GET','POST'])
def addTableData():
	if flask.request.method == 'POST':
		tempattr = ""
		tempvalue =[]
		for i in flask.session['tableAttr']:
			tempattr +=i[0]
			tempattr += ","
			tempvalue.append(flask.request.form.get(i[0]))
		sqlattr = tempattr.rsplit(',',1)[0]
		sqlvalue = tuple(tempvalue)
		sql = "insert into "+flask.session['tablename']+"("+sqlattr+")  values"+str(sqlvalue)+";" 
		connect = connectDatabase.connect()
		connect.begin()
		cursor = connect.cursor()
		try:	 
			cursor.execute(sql)
			connect.commit()
			return "ok"
		except:
			connect.rollback()
			return "错误"
		finally:
			cursor.close()
			connect.close()
	return flask.render_template('addtabledata.html',tablename=flask.session['tablename'],tableattr=flask.session['tableAttr'])


@app.route('/admin/table/data/look')
def lookTableData():
	tablename = flask.session['tablename']
	connect = connectDatabase.connect()
	cursor = connect.cursor()
	try:
		cursor.execute('select * from '+tablename+';')
		tablevalue = cursor.fetchall()
		return flask.render_template('looktabledata.html',tablename=tablename,tableattr=flask.session['tableAttr'],tablevalue=tablevalue)
	except:
		connect.rollback()
		return '数据异常'
	finally:
		cursor.close()
		connect.close()

@app.route('/admin/table',methods=['GET','POST'])
def addtable():
	if flask.request.method == "POST":
		tablename = flask.request.form.get('tablename')
		sql = "create table "+ tablename+"(id int(2) not null,"
		count =int(flask.request.form.get('attributeCount'))
		i = 0
		while i < count:
			attribute = flask.request.form.get('attribute'+str(i))
			texttype = flask.request.form.get('texttype'+str(i))
			length = flask.request.form.get('length'+str(i))
			isNull = flask.request.form.get('isNull'+str(i))
			tempSql = attribute+"  "+texttype+"("+str(length)+" )  "+isNull+","
			sql +=tempSql
			i += 1
		sql +='primary key(id));'
		connect = connectDatabase.connect()
		connect.begin()
		cursor = connect.cursor()
		try:
			cursor.execute(sql)
			connect.commit()
			return flask.redirect('/admin/')
		except:
			connect.rollback()
			return flask.redirect('/admin/table')
		finally:
			cursor.close()
			connect.close()
	return flask.render_template('addtable.html')


@app.route('/admin/user',methods=['GET','POST'])
def adduser():
	if flask.request.method == 'POST':
		username = flask.request.form.get('username')
		password = flask.request.form.get('password')
		connect = connectDatabase.connect()
		cursor = connect.cursor()
		try:
			cursor.execute("select password from users where username=%s;",(username))
			getpassword  = cursor.fetchall()
			if getpassword[0]:
				return "用户名已存在！"
		except:
			cursor.execute("insert into users(username,password) values(%s,%s);",(username,password))
			connect.commit()
			return flask.redirect('/admin/')
		finally:
			cursor.close()
			connect.close()
	return flask.render_template('adduser.html')


@app.route('/admin/user/update',methods=["POST"])
def updateUser():
	if flask.request.method == "POST":
		username = flask.request.form.get("username")
		flask.session['username'] = username
		return "跳转到修改密码界面"

@app.route('/admin/user/updating', methods=["POST","GET"])
def updating():
	if flask.request.method == "POST":
		username = flask.request.form.get('username')
		password = flask.request.form.get('password')
		sql = "update users set password=%s where username=%s;"
		connect = connectDatabase.connect()
		connect.begin()
		cursor = connect.cursor()
		try:
			cursor.execute(sql,(password,username))
			connect.commit()
			return flask.redirect('/admin/')
		except:
			connect.rollback()
			return "密码更新失败"
		finally:
			cursor.close()
			connect.close()
	return flask.render_template('updateUser.html',username=flask.session['username'])



@app.route('/admin/table/del',methods=["POST"])
def delTable():
	if flask.request.method == "POST":
		tablename = flask.request.form.get("tablename")
		sql = "drop table "+tablename+";"
		import droptable
		try:
			droptable.drop(sql)
			return "表删除成功"
		except:
			return "表删除失败"

@app.route('/admin/user/del',methods=['POST'])
def delUser():
	if flask.request.method == "POST":
		username = flask.request.form.get("username")
		connect = connectDatabase.connect()
		connect.begin()
		cursor = connect.cursor()
		sql = "delete from users where username=%s;"
		try:
			cursor.execute(sql,(username))
			connect.commit()
			return "用户删除成功"
		except:
			connect.rollback()
			return "用户删除失败"
		finally:
			cursor.close()
			connect.close()



@app.route('/user/register',methods=["GET","POST"])
def register():
	systemvalue = getsystemvalue()
	sqluser = 'insert into users(username,password,quanxian,infor_id) values(%s,%s,%s,%s);'
	sqlinfor = "insert into userinformation(name,birthday,xueli,gender) values(%s,%s,%s,%s);"
	if flask.request.method == 'POST' :
		username = flask.request.form.get('username')
		#判断用户名是否过于简单
		if len(username) <=6:
			print("你的用户名过于简单!")
			return flask.render_template("register.html")
		password = flask.request.form.get('password')
		#判断密码是否包含数字和字母
		if password.isnumeric() or password.isalpha():
			print("你的密码应该含有数字和字母!")
			return flask.render_template('register.html')
		quanxian = flask.request.form.get('user')
		connect = connectDatabase.connect()
		#开启事物处理
		connect.begin()
		try:
			cursor = connect.cursor()
			try:
				#查询用户是否被注册
				cursor.execute("select password from users where username=%s;",(username))
				data = cursor.fetchall()
				if data[0]:
					return "你的账号已经被注册了!"
			except:
				name = flask.request.form.get('uname')
				birthday = flask.request.form.get('birthday')
				xueli = flask.request.form.get('xueli')
				gender = flask.request.form.get('gender')
				cursor.execute(sqlinfor,(name,birthday,xueli,gender))
				#查询userinformation ID
				sqlSel = "select id from userinformation where name=%s;"
				cursor.execute(sqlSel,(name))
				infor_id = cursor.fetchone()[0]
				cursor.execute(sqluser,(username,password,quanxian,infor_id))
				connect.commit()
				return flask.redirect('/user/login')				

		except:
			connect.rollback()
			return "注册失败，可能原因是你的用户名或者密码过长！"
		finally:
			cursor.close()
			connect.close()
	return flask.render_template('register.html',systemvalue=systemvalue)

@app.route('/user/login',methods=['GET','POST'])
def login():
	systemvalue = getsystemvalue()
	if flask.request.method=="POST":
		username = flask.request.form.get('username')
		password = flask.request.form.get('password')
		goAdmin = flask.request.form.get('goAdmin')
		check = flask.request.form.get('check').lower()
		#验证两个验证码是否相等
		if check == flask.session['randomcheck']:
			#查询是否有这个用户
			connect = connectDatabase.connect()
			connect.begin()
			cursor=connect.cursor()
			sql = "select password,quanxian from users where username=%s;"
			try:
				cursor.execute(sql,(username))
				result = cursor.fetchone()
				getPassword = result[0]
				quanxian = result[1]
				connect.commit()
				#验证密码是否相等
				if password == getPassword:
					#查看权限等级
					if quanxian == 1:
						flask.session['username']=username
						if goAdmin == "1":
							return flask.redirect('/admin/'+username)
						return flask.redirect('/'+username)
					flask.session['username'] = username
					return flask.redirect('/'+username)
				return "密码错误!"
			except:
				connect.rollback()
				return "用户名不存在!"
			finally:
				cursor.close()
				connect.close()
		return "验证码错误!"
	randomcheck=""
	i=0
	while i<3:
		randomcheck += chr(random.randint(97,122))
		i += 1
	randomcheck += chr(random.randint(48,57))
	flask.session["randomcheck"] = randomcheck
	return flask.render_template('login.html',randomcheck=randomcheck,systemvalue=systemvalue)

@app.route('/user/information',methods=["GET","POST"])
def getInformation():
	systemvalue=getsystemvalue()
	if flask.request.method == "POST":
		username = flask.request.form.get('username')
		connect = connectDatabase.connect()
		cursor = connect.cursor()
		sql = "select a.username,a.password,a.quanxian,b.name,b.birthday,b.xueli,b.gender from users a left join userinformation b on a.infor_id=b.id where a.username=%s;"
		try:
			cursor.execute(sql,(username))
			nowValue = cursor.fetchone()
			flask.session['tempInfor']=nowValue
			return 'ok'
		except:
			return 'error'
		finally:
			cursor.close()
			connect.close()
	return flask.render_template('userinformation.html',information=flask.session['tempInfor'],systemvalue=systemvalue)

@app.route('/system/set',methods=['POST','GET'])
def systemSet():
	if flask.request.method=="POST":
		bg = flask.request.form.get('bg')
		bgmusic = flask.request.form.get('bgmusic')
		transparency = flask.request.form.get('transparency')
		fontsize = flask.request.form.get('fontsize')
		fontcolor = flask.request.form.get('fontcolor')
		sysvalue.update({'bg':bg})
		sysvalue.update({'bgmusic':bgmusic})
		sysvalue.update({'transparency':transparency})
		sysvalue.update({'fontsize':fontsize})
		sysvalue.update({'fontcolor':fontcolor})
		flask.session['system'] = sysvalue
		try:
			username = flask.session['username']
			return flask.redirect('/'+username)
		except:
			return flask.redirect('/')
	systemvalue = getsystemvalue()
	return flask.render_template('systemset.html',systemvalue=systemvalue)

@app.route('/system/returnIndex')
def systemSetReturnIndex():
	try:
		username = flask.session['guest'] or flask.session['username']
		return username
	except:
		return ""

@app.route('/system/help/<username>')
def returnHelp(username):
	return flask.render_template('help.html',username=username)

@app.route("/system/dealData",methods=["POST"])
def deal_data():
	content=flask.request.form.get("content")
	filename="data/data.txt"
	X_train,y_train,lens,answer_vocabulary=getData(filename)
	with open("data/question.txt","r+",encoding="utf-8") as f:
		question_result=f.read()
	questions=question_result.split("\n")
	with open("data/answer.txt","r+",encoding="utf-8") as f:
		answer_result=f.read()
	answers=answer_result.split("\n")
	l=0
	question_len=len(questions)
	while l<question_len:
		if questions[l]==content:
			return answers[l]
		l += 1
	knn=data_train(X_train,y_train,lens)
	X_test=[[]]
	try:
		for temp in jieba.cut(content):
			X_test[0].append(question_vocabulary[temp])
	except:
		X_test[0].append(0)
	templen=len(X_test[0])
	temparray=[[]]
	if templen < lens:
		for i in X_test[0]:
			temparray[0].append(i)
		while templen<lens:
			temparray[0].append(-1)
			templen+=1
	else:
		i=0
		while i<lens:
			temparray[0].append(X_test[0][i])
			i+=1
	y_predict = knn.predict(temparray)
	ans=""
	for temp_index in y_predict:
		ans+=answer_result[temp_index]
	if ans == "":
		return "这个问题我还不会，太难了"
	return ans
if __name__ == '__main__':
	app.run(debug=True)